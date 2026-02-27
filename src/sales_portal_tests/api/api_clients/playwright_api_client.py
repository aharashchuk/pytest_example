"""Playwright-backed concrete implementation of :class:`BaseApiClient`."""

from __future__ import annotations

import json
from typing import Any

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from sales_portal_tests.api.api_clients.base_api_client import BaseApiClient
from sales_portal_tests.data.models.core import RequestOptions, Response
from sales_portal_tests.utils.mask_secrets import mask_secrets


class PlaywrightApiClient(BaseApiClient):
    """HTTP client powered by Playwright's :class:`APIRequestContext`.

    Each call to :meth:`send` is wrapped in an Allure step and produces two
    attachments — the masked request payload and the response body — which are
    visible in the Allure report.

    Args:
        api_context: A Playwright ``APIRequestContext`` instance (typically
                     obtained from ``playwright.request.new_context()``).
    """

    def __init__(self, api_context: APIRequestContext) -> None:
        self._api_context = api_context

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def send(self, options: RequestOptions) -> Response[object | None]:
        """Execute an HTTP request described by *options* and return a typed response.

        The method:

        1. Builds the ``fetch`` keyword arguments from *options*.
        2. Executes the request via ``APIRequestContext.fetch()``.
        3. Transforms the raw ``APIResponse`` into a :class:`Response`.
        4. Attaches the (masked) request and response JSON to the current
           Allure step.

        Args:
            options: :class:`~sales_portal_tests.data.models.core.RequestOptions`
                     describing the HTTP call.

        Returns:
            A typed :class:`~sales_portal_tests.data.models.core.Response`.

        Raises:
            playwright.sync_api.Error: Propagated from Playwright on network failures.
        """
        step_title = f"Request {options.method.upper()} {options.url}"

        with allure.step(step_title):
            fetch_kwargs = self._build_fetch_kwargs(options)
            raw: APIResponse = self._api_context.fetch(options.url, **fetch_kwargs)
            response = self._transform_response(raw)

            self._attach_request(options)
            self._attach_response(response)

            return response

    # ------------------------------------------------------------------
    # BaseApiClient abstract methods
    # ------------------------------------------------------------------

    def _transform_response(self, raw_response: Any) -> Response[object | None]:
        """Convert a Playwright ``APIResponse`` into a typed :class:`Response`.

        Attempts to decode the body as JSON; falls back to plain text when the
        ``Content-Type`` header is not ``application/json``.

        Args:
            raw_response: A ``playwright.sync_api.APIResponse`` instance.

        Returns:
            A :class:`Response` with ``status``, ``headers`` and ``body``.
        """
        raw: APIResponse = raw_response
        content_type: str = raw.headers.get("content-type", "")

        if "application/json" in content_type:
            body: object | None = raw.json()
        else:
            text = raw.text()
            body = text if text else None

        return Response(
            status=raw.status,
            headers=dict(raw.headers),
            body=body,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_fetch_kwargs(options: RequestOptions) -> dict[str, Any]:
        """Build the keyword arguments dict accepted by ``APIRequestContext.fetch``.

        Args:
            options: Request description.

        Returns:
            A dict suitable for ``**fetch_kwargs`` unpacking.
        """
        kwargs: dict[str, Any] = {"method": options.method}

        if options.headers:
            kwargs["headers"] = options.headers

        if options.data is not None:
            kwargs["data"] = options.data

        if options.params is not None:
            kwargs["params"] = options.params

        return kwargs

    def _attach_request(self, options: RequestOptions) -> None:
        """Attach the (masked) request payload to the current Allure step.

        Args:
            options: The request options used for the call.
        """
        payload: dict[str, Any] = {}
        if options.headers:
            payload["headers"] = options.headers
        if options.data is not None:
            payload["body"] = options.data
        if options.params is not None:
            payload["params"] = options.params

        raw_json = json.dumps(payload, indent=2, default=str)
        masked_json = mask_secrets(raw_json)

        allure.attach(
            masked_json,
            name="request.json",
            attachment_type=allure.attachment_type.JSON,
        )

    def _attach_response(self, response: Response[object | None]) -> None:
        """Attach the (masked) response payload to the current Allure step.

        Args:
            response: The typed response returned by :meth:`_transform_response`.
        """
        payload: dict[str, Any] = {
            "status": response.status,
            "headers": response.headers,
            "body": response.body,
        }

        raw_json = json.dumps(payload, indent=2, default=str)
        masked_json = mask_secrets(raw_json)

        allure.attach(
            masked_json,
            name="response.json",
            attachment_type=allure.attachment_type.JSON,
        )
