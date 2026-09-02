# Capslane Python SDK

The Capslane Python SDK retrieves YouTube transcripts from Python applications. It returns existing captions when available and can generate a transcript when a video has no usable caption track. The package uses the Python standard library and has no runtime dependency.

## Requirements

- Python 3.10 or later
- A Capslane API key from the [dashboard](https://capslane.com/api-keys)

## Installation

```bash
pip install capslane
```

## Retrieve a transcript

```python
import os

from capslane import CapslaneClient

capslane = CapslaneClient(os.environ["CAPSLANE_API_KEY"])

result = capslane.transcript(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    mode="auto",
)

transcript = (
    capslane.wait_for_transcript(result)
    if "jobId" in result
    else result
)

print(transcript["content"])
```

## Check a transcript job

```python
job = capslane.transcript_job(
    "job_00000000-0000-0000-0000-000000000000"
)
```

`wait_for_transcript` polls an accepted job until it completes, fails or reaches the timeout.

```python
transcript = capslane.wait_for_transcript(
    job,
    interval=2.0,
    timeout=20 * 60,
)
```

## Request options

| Option | Type | Description |
| --- | --- | --- |
| `url` | `str` | Public YouTube URL or 11-character video ID. |
| `lang` | `str` | Optional preferred language code. |
| `mode` | `native`, `auto` or `generate` | Selects how Capslane obtains the transcript. |
| `text` | `bool` | Returns one text string instead of timestamped segments. |
| `chunk_size` | `int` | Groups transcript segments into larger chunks. |

## Modes

- `native` returns existing captions and never starts speech transcription.
- `auto` uses existing captions first and generates a transcript only when needed.
- `generate` creates a transcript from the video audio.

## Errors

Failed requests raise `CapslaneError`. The error includes the HTTP status, Capslane error code and request ID when available.

```python
from capslane import CapslaneError

try:
    capslane.transcript("invalid")
except CapslaneError as error:
    print(error.status, error.code, error.request_id)
```

## Security

Use Capslane from a trusted server. Do not expose API keys in browser code, public repositories or client-side environment variables.

## Links

- [Documentation](https://capslane.com/docs)
- [API reference](https://capslane.com/api-reference)
- [Dashboard](https://capslane.com/dashboard)
- [GitHub](https://github.com/WebbaLuca/capslane-python)

## License

MIT
