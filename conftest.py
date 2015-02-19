import pytest

from django.utils.translation import (
    activate as activate_language, deactivate as deactivate_language)


@pytest.yield_fixture()
def activate_en():
    activate_language('en')
    yield
    deactivate_language()
