from datetime import datetime
from typing import Any, Callable, Iterable, Optional

from typing_extensions import NotRequired, TypedDict

# TODO: Recursive type hints not yet available in mypy,
#  should change sub_fields hint to Optional[List[FieldConfig]] when possible:
#  https://github.com/python/mypy/issues/731
FieldConfig = TypedDict(
    'FieldConfig',
    {
        'field_name': str,
        'limit': NotRequired[int],
        'after': NotRequired[str],
        'sub_fields': NotRequired[list[Any]],
    },
)


def format_fields_str(fields_config: list[FieldConfig]) -> str:
    """
    Helper function to support field expansion / limiting functionality:
    https://developers.facebook.com/docs/graph-api/field-expansion
    :param fields_config: The field configurations you want contained in string format
    :return: A formatted fields string
    """
    fields_str = ''
    for config in fields_config:
        # Prep the base sub string for a field (i.e. foo.limit(5).after(BAR))
        limit_sub_str = _format_field_config_paging_sub_str(config, 'limit')
        after_sub_str = _format_field_config_paging_sub_str(config, 'after')
        fields_str += f'{config["field_name"]}{limit_sub_str}{after_sub_str}'

        # If sub-fields exist, prep the nested sub field(s) strings
        sub_fields = config.get('sub_fields')
        if sub_fields:
            fields_str += f'{{{format_fields_str(sub_fields)}}}'

        # If not the last item in a config list, add a comma separator
        if config != fields_config[-1]:
            fields_str += ','
    return fields_str


def _format_field_config_paging_sub_str(config: FieldConfig, param_name: str) -> str:
    """
    Used to help format paging sub strings for a specific field:
    https://developers.facebook.com/docs/graph-api/field-expansion#limiting-results
    :param config: An instance of FieldConfig
    :param param_name: The parameter name to pluck from config (i.e. limit or after)
    :return: A formatted paging sub string (i.e. .limit(5))
    """
    param = config.get(param_name)
    return f'.{param_name}({param})' if param else ''


def posix_2_datetime(timestamp: int) -> datetime:
    """
    Convert POSIX timestamp to datetime
    :param timestamp: POSIX timestamp
    :return: Resulting datetime obj
    """
    return datetime.utcfromtimestamp(timestamp / 1000)


def first_true(
    iterable: Iterable[Any], pred: Callable, default: Optional[Any] = None
) -> Optional[Any]:
    """
    Find the first occurrence of something matching a predicate with default value
    :param iterable: Iterable containing items to match
    :param pred: Predicate containing matching logic
    :param default: Default value if no match found
    :return: Matching item or default
    """
    return next(filter(pred, iterable), default)
