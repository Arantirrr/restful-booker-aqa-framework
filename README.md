[![Tests](https://github.com/Arantirrr/restful-booker-aqa-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Arantirrr/restful-booker-aqa-framework/actions/workflows/tests.yml)

# Restful Booker AQA Framework

API test automation framework for restful-booker-platform.

## Tech Stack

* Python 3.13
* pytest
* requests
* pydantic
* pydantic-settings

## Project Structure

```text
restful-booker-aqa-framework/
├── .github/
│   └── workflows/
│       └── tests.yml             # GitHub Actions workflow for smoke and regression tests
├── clients/                      # HTTP transport and API client implementations
│   ├── base_client.py
│   ├── auth_client.py
│   └── booking_client.py
├── config/                       # Environment-driven application configuration
│   └── settings.py
├── models/                       # Pydantic models defining API request and response contracts
│   ├── booking.py
│   └── booking_errors.py
├── tests/                        # Automated API tests and test data
│   ├── booking/
│   │   ├── conftest.py
│   │   └── test_booking.py
│   ├── data/
│   │   ├── booking_data.py
│   │   └── __init__.py
│   └── conftest.py
├── .env.example                  # Example environment configuration
├── .gitignore                    # Git ignore rules
├── conftest.py                   # Shared pytest configuration and fixtures
├── main.py                       # Scratchpad for local experiments (not part of the framework)
├── pytest.ini                    # Pytest configuration and markers
├── requirements-dev.txt          # Development and test dependencies
└── requirements.txt              # Runtime dependencies
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Arantirrr/restful-booker-aqa-framework.git
cd restful-booker-aqa-framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (cmd)

```cmd
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Create `.env` from `.env.example`.

### Windows (PowerShell)

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Then configure the required environment variables in `.env`:

```env
API_URL=https://example.com/api
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
ENV=dev
```

## Running Tests

Run the complete test suite:

```bash
pytest -v tests/
```

Run smoke tests:

```bash
pytest -v tests/ -m smoke
```

Run regression tests:

```bash
pytest -v tests/ -m regression
```

Run positive tests:

```bash
pytest -v tests/ -m positive
```

Run negative tests:

```bash
pytest -v tests/ -m negative
```

### Pytest Markers

| Marker       | Description                            |
| ------------ | -------------------------------------- |
| `smoke`      | Quick checks that the service is alive |
| `regression` | Full test suite                        |
| `positive`   | Happy-path tests                       |
| `negative`   | Tests for error handling               |

## Architecture

The framework is organized in layers:

* **`clients/`** — HTTP transport. `BaseClient` provides common request logic, while domain-specific clients such as `AuthClient` and `BookingClient` implement API operations.
* **`models/`** — Pydantic models describing API contracts for requests, responses, and error payloads.
* **`tests/`** — Business logic checks. Tests are grouped by domain, with booking scenarios located in `tests/booking/`.
* **`config/`** — Environment-driven settings managed with `pydantic-settings`.
