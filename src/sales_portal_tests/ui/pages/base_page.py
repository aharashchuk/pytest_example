"""Abstract base page — network interception helpers, cookie utilities, lock assertions."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from playwright.sync_api import Locator, Page, expect

from sales_portal_tests.data.models.core import Response
from sales_portal_tests.utils.report.allure_step import step

T = TypeVar("T")


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def intercept_request(
        self,
        url: str,
        trigger_action: Callable[..., None],
        *args: Any,
    ) -> Any:
        """Wait for a request matching *url* while calling *trigger_action*."""
        with self.page.expect_request(lambda req: url in req.url) as request_info:
            trigger_action(*args)
        return request_info.value

    def intercept_response(
        self,
        url: str,
        trigger_action: Callable[..., None],
        *args: Any,
    ) -> Response[Any]:
        """Wait for a response matching *url* while calling *trigger_action*."""
        with self.page.expect_response(lambda resp: url in resp.url) as response_info:
            trigger_action(*args)
        raw = response_info.value
        return Response(
            status=raw.status,
            headers=dict(raw.headers),
            body=raw.json(),
        )

    def expect_request(
        self,
        method: str,
        url: str,
        query_params: dict[str, str],
        trigger_action: Callable[..., None],
        *args: Any,
    ) -> None:
        """Assert that a request with given *method*, *url* and *query_params* is fired."""

        def _matches(req: Any) -> bool:
            if not (url in req.url and req.method == method.upper()):
                return False
            return all(f"{k}={v}" in req.url for k, v in query_params.items())

        with self.page.expect_request(_matches) as request_info:
            trigger_action(*args)
        assert request_info.value is not None

    @step("GET AUTH TOKEN FROM COOKIES")
    def get_auth_token(self) -> str:
        """Return the value of the *Authorization* cookie."""
        cookies = self.page.context.cookies()
        cookie = next((c for c in cookies if c["name"] == "Authorization"), None)
        assert cookie is not None, "Authorization cookie not found"
        return str(cookie["value"])

    @step("GET COOKIE BY NAME")
    def get_cookie_by_name(self, name: str) -> dict[str, Any] | None:
        """Return the first cookie matching *name*, or *None*."""
        cookies = self.page.context.cookies()
        result = next((c for c in cookies if c["name"] == name), None)
        return dict(result) if result is not None else None

    @step("FIELD IS DISABLED")
    def expect_locked(self, input_locator: Locator) -> None:
        """Assert that *input_locator* is either disabled or read-only."""
        if input_locator.is_disabled():
            expect(input_locator).to_be_disabled()
        else:
            expect(input_locator).to_have_js_property("readOnly", True)
