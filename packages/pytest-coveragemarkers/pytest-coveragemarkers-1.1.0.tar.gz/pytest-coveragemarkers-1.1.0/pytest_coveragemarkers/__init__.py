"""
pytest_coveragemarkers

isort:skip_file
"""
import os
import sys

from loguru import logger

from .process_marker_spec import load_yaml

from .filter_engine import check_rules, overall_result
from .plugin import (
    InvalidMarkerValue,
    reformat_cov_marker,
    reformat_cov_marker_args,
    validate_marker_values,
)


logger.remove()
logger.add(
    sys.stderr, level=os.getenv("PYTEST_COVMRK_LOG_LEVEL", default="DEBUG")
)  # pragma: nocover


__all__ = [
    "load_yaml",
    "check_rules",
    "overall_result",
    "reformat_cov_marker",
    "reformat_cov_marker_args",
    "validate_marker_values",
    "InvalidMarkerValue",
    "logger",
]  # pragma: nocover
