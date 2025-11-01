# Keycrate SDK - Python Examples

Simple and full examples for the Keycrate license authentication SDK in Python.

## Prerequisites

-   Python 3.7 or higher

## Setup

Install the Keycrate package:

```bash
pip install keycrate
```

## Running

```bash
python main.py
```

## Examples

-   **Simple Example** - Basic authentication with license key or username/password, plus registration
-   **Full Example** - Includes HWID detection, detailed error handling, and a post-login menu

## Configuration

Update the app ID in `main.py`:

```python
client = keycrate.configurate(
    host="https://api.keycrate.dev",
    app_id="YOUR_APP_ID"
)
```

## Dependencies

-   **keycrate** - Keycrate SDK
