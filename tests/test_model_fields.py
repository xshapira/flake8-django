import pytest

from flake8_django.checkers.model_fields import NOT_NULL_TRUE_FIELDS

from .utils import run_check, error_code_in_result


@pytest.mark.parametrize('field_type', NOT_NULL_TRUE_FIELDS)
def test_not_null_fields_fails(field_type):
    code = f"field = models.{field_type}(null=True)"
    result = run_check(code)
    assert error_code_in_result('DJ01', result)


@pytest.mark.parametrize('field_type', NOT_NULL_TRUE_FIELDS)
def test_not_null_fields_success(field_type):
    code = f"field = models.{field_type}()"
    result = run_check(code)
    assert not error_code_in_result('DJ01', result)


@pytest.mark.parametrize('field_type', NOT_NULL_TRUE_FIELDS)
def test_null_fields_with_unique_true_success(field_type):
    code = f"field = models.{field_type}(null=True, unique=True, blank=True)"
    result = run_check(code)
    assert not error_code_in_result('DJ01', result)


@pytest.mark.parametrize('field_type', NOT_NULL_TRUE_FIELDS)
def test_blank_as_an_expression_does_not_raise_an_error(field_type):
    code = f"field = models.{field_type}(null=True, blank=not settings.SETTING)"
    result = run_check(code)
    assert error_code_in_result('DJ01', result)
