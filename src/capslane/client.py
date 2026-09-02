from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class CapslaneError(Exception):
    status: int
    code: str
    message: str
    request_id: str | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class CapslaneClient:
    def __init__(self, api_key: str, base_url: str = "https://capslane.com", timeout: float = 20.0) -> None:
        if not api_key.strip():
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def transcript(
        self,
        url: str,
        *,
        lang: str | None = None,
        text: bool | None = None,
        chunk_size: int | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        query: dict[str, str] = {"url": url}
        if lang:
            query["lang"] = lang
        if text is not None:
            query["text"] = str(text).lower()
        if chunk_size is not None:
            query["chunkSize"] = str(chunk_size)
        if mode:
            query["mode"] = mode
        return self._get(f"/v1/transcript?{urlencode(query)}")

    def transcript_job(self, job_id: str) -> dict[str, Any]:
        return self._get(f"/v1/transcript/{job_id}")

    def wait_for_transcript(
        self,
        job: dict[str, Any] | str,
        *,
        interval: float = 2.0,
        timeout: float = 20 * 60,
    ) -> dict[str, Any]:
        job_id = job if isinstance(job, str) else str(job["jobId"])
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            time.sleep(interval)
            result = self.transcript_job(job_id)
            if "content" in result:
                return result
            if result.get("status") in {"failed", "cancelled"}:
                raise CapslaneError(422, str(result.get("error", result["status"])), f"Transcript job {result['status']}", result.get("requestId"))
        raise CapslaneError(504, "processing_timeout", "Transcript job deadline exceeded")

    def _get(self, path: str) -> dict[str, Any]:
        request = Request(
            f"{self.base_url}{path}",
            headers={"x-api-key": self.api_key, "accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            body = self._error_body(error)
            raise CapslaneError(error.code, str(body.get("error", "request_failed")), str(body.get("message", "Capslane request failed")), body.get("requestId")) from error
        except URLError as error:
            raise CapslaneError(0, "network_error", str(error.reason)) from error

    @staticmethod
    def _error_body(error: HTTPError) -> dict[str, Any]:
        try:
            return json.loads(error.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"error": "request_failed", "message": "Capslane request failed"}
