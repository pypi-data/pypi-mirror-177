import operator

from . import logger


class InvalidQuery(Exception):
    pass


class Filter:
    attr_separator = "."
    binary_operators = {
        "=": operator.eq,
        "==": operator.eq,
        "eq": operator.eq,
        "!=": operator.ne,
        "ne": operator.ne,
    }

    multiple_operators = {
        "or": any,
        "and": all,
    }

    def __init__(self, filtering):
        self._filtering = filtering
        self._eval = self._evaluator(filtering)  # pragma: nocover

    def __call__(self, **kwargs):
        try:  # pragma: nocover
            return self._eval(kwargs)
        except TypeError as exc:
            logger.exception(exc)
            raise InvalidQuery(self._filtering)

    def _evaluator(self, filtering):
        try:  # pragma: nocover
            operator_, nodes = list(filtering.items())[0]
        except (AttributeError, IndexError) as exc:
            logger.exception(exc)
            return False

        try:  # pragma: nocover
            op = self.multiple_operators[operator_]
        except KeyError:
            try:  # pragma: nocover
                op = self.binary_operators[operator_]
            except KeyError as exc:
                logger.exception(exc)
                return False
            if len(nodes) != 2:
                # binary operators take 2 values
                return False

            def _op(values):
                try:  # pragma: nocover
                    return op(self._resolve_name(values, nodes[0]), nodes[1])
                except Exception:
                    # we didn't get a rule match so return False
                    return False

            return _op

        # Iterate over every item in the list of the value linked
        # to the logical operator, and compile it down to its own
        # evaluator.
        elements = [self._evaluator(node) for node in nodes]
        return lambda values: op(e(values) for e in elements)

    def _resolve_name(self, values, name):
        logger.debug(f"Resolving name: {name} into {values}")
        try:  # pragma: nocover
            for subname in name.split(self.attr_separator):
                values = values[subname]
            return values
        except KeyError:
            raise InvalidQuery(f"Unknown attribute {name}")


def check_rules(rules, data):
    try:
        x = [Filter(r)(**data) for r in rules]
        logger.info("Checking rules {} on {} resulted in {}", rules, data, x)
        return all(x)
    except InvalidQuery as exc:
        logger.exception(exc)
        return False



def overall_result(results):
    if not results:
        return False
    checks = []
    for r in results:
        if isinstance(r, list):
            checks.append(all(r))
        else:
            checks.append(r)
    return all(checks)
