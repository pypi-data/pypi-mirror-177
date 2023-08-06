import json
import os
from typing import List, Optional, Set, Tuple, Union
from pathlib import Path

import pytest

from . import check_rules, load_yaml, logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__name__))


class InvalidMarkerValue(AssertionError):
    """ """

    pass


def pytest_addoption(parser):

    group = parser.getgroup("coveragemarkers")
    # Filter section
    group.addoption(
        "--filter", action="store", help="Filtering of tests by coverage marker."
    )
    filter_location_help = "JSON File location of filter specifications."
    group.addoption(
        "--filter-location",
        action="store",
        dest="filterlocation",
        help=filter_location_help,
    )
    parser.addini(
        "FilterLocation",
        filter_location_help,
    )

    # Specification section
    default_markers = os.path.join("marker_specs", "coverage_markers.yml")
    markers_location_help = "Yaml File location of marker specifications."
    group.addoption(
        "--markers-location",
        action="store",
        dest="markerslocation",
        help=markers_location_help,
    )
    parser.addini(
        "MarkersLocation",
        markers_location_help,
        default=default_markers,
    )


def _determine_marker_path(config):
    _markers_location = config.getoption("markerslocation") or config.getini(
        "MarkersLocation"
    )
    markers_location = os.path.join(config.rootdir, _markers_location)
    logger.debug(f"Checking for marker yml at: {markers_location}")
    if os.path.exists(markers_location):
        return markers_location

    logger.debug(f"Failed to find markers at: {markers_location}. Trying elsewhere...")
    markers_location = os.path.join(
        SCRIPT_DIR, "pytest_coveragemarkers", _markers_location
    )
    logger.debug(f"Checking for marker yml at: {markers_location}")
    if os.path.exists(markers_location):
        return markers_location


def pytest_configure(config):
    markers_spec = {}

    markers_location = _determine_marker_path(config=config)

    logger.info("Loading master marker yml file: {}", markers_location)
    load_yaml(markers_spec, markers_location)

    done = {}
    for marker in markers_spec.get("markers", []):
        marker_name = marker.get("name", "")
        if marker_name:
            logger.info("Including marker name: {}", marker_name)
            done[marker_name] = marker
            config.addinivalue_line("markers", marker_name)
    setattr(config, "cov_markers", done)


def pytest_report_header(config):
    lines = []
    cov_filter = config.getoption("--filter")
    if cov_filter:
        lines.append(f"coverage filter: {cov_filter}")
    markers_location = config.getoption("markerslocation") or config.getini(
        "MarkersLocation"
    )
    if markers_location:
        lines.append(f"Cov Markers: {markers_location}")
    return lines


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    # update test items with cw_metadata
    update_test_with_cov_markers(items)
    apply_filter_rule(config, items)


@pytest.mark.optionalhook
def pytest_json_runtest_metadata(item):
    return {"cov_markers": item.cov_markers} if hasattr(item, "cov_markers") else {}


def update_test_with_cov_markers(items):
    """
    Loop through all test items and update their metadata
    """

    for item in items:
        if not hasattr(item, "cov_markers"):
            item.cov_markers = {}
        for mark in item.iter_markers():
            if is_coverage_marker(mark, item.config):
                updates_ = reformat_cov_marker(mark)
                item.cov_markers.update(updates_)
        # output to json report
        content = json.dumps(item.cov_markers)
        logger.debug("Recording markers for test: {}", content)
        item.add_report_section("setup", "_metadata", content)


def is_coverage_marker(marker, config):
    logger.debug("Checking if '{}' in {}", marker.name, list(config.cov_markers.keys()))
    if marker.name in list(config.cov_markers.keys()):
        return True
    return False


def reformat_cov_marker(marker):
    arguments = {}
    for val in reformat_cov_marker_args(marker):
        arguments[val] = True
    return {marker.name: arguments}


def reformat_cov_marker_args(marker):
    """
    Processes the args supplied to a fixture in order to return a simplified
    list containing the args

    """
    # args in format (['value1', 'value2', ...],) so simplify to just a list
    simplified = []
    marker_args = ensure_list(marker.args)
    # TODO: check we still need these!
    if isinstance(marker.args, str):
        marker_args = [marker.args]
    if isinstance(marker.args, bool):
        marker_args = [marker.args]
    if isinstance(marker.args, tuple):
        marker_args = marker.args[0]

    for arg in marker_args:
        if arg:
            if isinstance(arg, list):
                simplified.extend(arg)
            else:
                simplified.append(arg)
    if not isinstance(simplified, list):
        # single value so wrap in list
        simplified = [simplified]
    logger.debug("Simplified '{}' to '{}'", marker.args, simplified)
    return simplified


def get_filter_json_location(config):
    # Check if filterlocation was provided instead
    _filter_location = config.getoption("filterlocation") or config.getini(
        "FilterLocation"
    )
    if not _filter_location:
        return False
    filter_location = os.path.join(config.rootdir, _filter_location)
    logger.debug(f"Checking for filter json at: {filter_location}")
    if os.path.exists(filter_location):
        return filter_location

    logger.debug(f"Failed to find filter json file at: {filter_location}. Trying elsewhere...")
    filter_location = os.path.join(
        SCRIPT_DIR, "pytest_coveragemarkers", _filter_location
    )
    logger.debug(f"Checking for marker yml at: {filter_location}")
    if os.path.exists(filter_location):
        return filter_location


def get_filter_json(filter_json_path):
    with Path(filter_json_path).open(encoding="UTF-8") as source:
        return json.load(source)


def apply_filter_rule(config, items):
    # check if you got an option like --filter='{"eq": {}}'
    not_in_group = pytest.mark.skip(
        reason="Test failed to meet filter rule criteria"
    )

    filter_arg = config.getoption("--filter")
    if filter_arg:
        logger.info("Applying filter: {}", filter_arg)
        filter_rule = json.loads(filter_arg)
        for item in items:
            if not check_rules(rules=[filter_rule], data=item.cov_markers):
                item.add_marker(not_in_group)
    else:
        filter_json = get_filter_json_location(config)
        if filter_json:
            filter_spec = get_filter_json(filter_json)
            logger.info("Applying filter: {}", filter_spec)
            if len(filter_spec) == 0:
                # Empty filter defined so no filtering applied
                return
            for item in items:
                if not check_rules(rules=[filter_spec], data=item.cov_markers):
                    item.add_marker(not_in_group)


@pytest.fixture(autouse=True)
def cov_markers(request):
    """fixture for setting gs_applicaton in test metadata"""
    # TODO: Need to pass in name and allowed_args into this fixture
    validate_marker_values(request)


def validate_marker_values(request):
    for mark in request.node.iter_markers():
        if not is_coverage_marker(mark, request.config):
            break

        allowed_values = request.config.cov_markers.get(mark.name, {}).get(
            "allowed", []
        )

        # no allowed_value so let everything through
        if not allowed_values:
            return

        if not check_values_in_list(
            source_value=mark.args[0], allowed_values=allowed_values
        ):
            raise InvalidMarkerValue(
                "<{}>: {} is a value not in {}".format(
                    mark.name, mark.args[0], allowed_values
                )
            )


def ensure_list(s: Optional[Union[str, List[str], Tuple[str], Set[str]]]) -> List[str]:
    # Ref: https://stackoverflow.com/a/56641168/
    return (
        s
        if isinstance(s, list)
        else list(s)
        if isinstance(s, (tuple, set))
        else []
        if s is None
        else [s]
    )


def check_values_in_list(source_value, allowed_values):
    """
    return True is all items in source_value are present in allowed_values

    :param source_value:
    :param allowed_values:
    :return: True | False
    """
    if not allowed_values:
        logger.debug("Empty allowed values so accepting source value as valid")
        return True

    logger.debug("Checking for '{}' in {}", source_value, allowed_values)
    source_value = ensure_list(source_value)
    if all(val in allowed_values for val in source_value):
        return True
    return False


def get_plugin_root_path():
    # package module installed
    from distutils.sysconfig import get_python_lib

    logger.info(f"{get_python_lib()=}")
    root_path = os.path.join(get_python_lib(), "pytest_coveragemarkers")
    logger.info(f"{root_path=}")
    if os.path.isdir(root_path):
        return root_path
    # try from this file
    root_path = os.path.join(
        os.path.dirname(os.path.abspath(__name__)), "pytest_coveragemarkers"
    )
    logger.info(f"{root_path=}")
    if os.path.isdir(root_path):
        return root_path
    # TODO: Custom exception please
    raise Exception("Cannot determine root path for Yaml files")
