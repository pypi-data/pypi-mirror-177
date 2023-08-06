# pyright: reportPrivateUsage=false
import pytest

from ..conftest import AsyncHttpClientMixin


async def test_using_client_after_exiting_context_manager_raises_runtime_error(
    async_http_client_mixin: AsyncHttpClientMixin,
):
    async with async_http_client_mixin:
        pass
    with pytest.raises(RuntimeError) as err_info:
        await async_http_client_mixin._http_client.get("")
    assert str(err_info.value) == "Cannot reopen HttpClientMixin instance once it has been closed"


async def test_using_client_after_manually_closing_raises_runtime_error(async_http_client_mixin: AsyncHttpClientMixin):
    await async_http_client_mixin.close()
    with pytest.raises(RuntimeError) as err_info:
        await async_http_client_mixin._http_client.get("")
    assert str(err_info.value) == "Cannot reopen HttpClientMixin instance once it has been closed"


async def test_using_client_in_context_manager_after_already_opening_raises_runtime_error(
    async_http_client_mixin: AsyncHttpClientMixin,
):
    with pytest.raises(RuntimeError) as err_info:
        async with async_http_client_mixin:
            async with async_http_client_mixin:
                ...
    assert str(err_info.value) == "Cannot open HttpClientMixin instance more than once"
