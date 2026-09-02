# Capslane Python SDK

Official server-side client for the Capslane YouTube transcript API. It uses the Python standard library and adds no runtime dependency.

```bash
pip install capslane
```

```python
import os
from capslane import CapslaneClient

capslane = CapslaneClient(os.environ["CAPSLANE_API_KEY"])
result = capslane.transcript("dQw4w9WgXcQ", mode="auto")
transcript = capslane.wait_for_transcript(result) if "jobId" in result else result
```

Keep the API key on a trusted server. See [Capslane documentation](https://capslane.com/docs) for the complete contract.
