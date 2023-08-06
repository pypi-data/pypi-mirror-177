# pyright: reportPrivateUsage=false
import pytest

from ..conftest import HttpClientMixin


def test_using_client_after_exiting_context_manager_raises_runtime_error(
    http_client_mixin: HttpClientMixin,
):
    with http_client_mixin:
        pass
    with pytest.raises(RuntimeError) as err_info:
        http_client_mixin._http_client.get("")
    assert str(err_info.value) == "Cannot reopen HttpClientMixin instance once it has been closed"


def test_using_client_after_manually_closing_raises_runtime_error(http_client_mixin: HttpClientMixin):
    http_client_mixin.close()
    with pytest.raises(RuntimeError) as err_info:
        http_client_mixin._http_client.get("")
    assert str(err_info.value) == "Cannot reopen HttpClientMixin instance once it has been closed"


def test_using_client_in_context_manager_after_already_opening_raises_runtime_error(
    http_client_mixin: HttpClientMixin,
):
    with pytest.raises(RuntimeError) as err_info:
        with http_client_mixin:
            with http_client_mixin:
                ...
    assert str(err_info.value) == "Cannot open HttpClientMixin instance more than once"
