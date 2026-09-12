# Compatibility and validation

Reviewed on 2026-09-12 from default branch `master`, baseline `282f097`.

## Baseline

- No README or license file was tracked. Source, YAML, Dockerfile, Makefile, two PEM files, and a database-writing unittest were present; no tracked dependency trees, caches, or compiled artifacts were found.
- `python3 test.py` on Python 3.12.6 failed importing `psycopg2`; the original environment was not installed. The old Dockerfile targets Ubuntu 18.04 and the 2020 manifest includes compiled packages predating Python 3.12.
- HTTP import pulled an unused CatBoost module, which imports undeclared SHAP. No complete ML installation/training path is verified.
- Both PEM files are byte-identical, parse as public X.509 certificates, and expired on 2021-05-03. No private-key marker was found in either file.

## Dependency changes

The HTTP requirements now contain only imports needed by the HTTP service. Python 3.12 compatibility is the reason for changing the old installation target; the original manifest is preserved as `requirements-legacy.txt`, without credentials.

| Component | Original → supported HTTP / optional polling target | Reason and behavior |
|---|---|---|
| Flask | 1.1.2 → 3.1.2 | Supported Python runtime; retain initialization and blueprints. `FlaskGroup(create_app=...)` fixes actual CLI app-discovery failure observed during schema creation. |
| Flask-Cors | 3.0.8 → 6.0.1 | Compatible Flask stack; existing broad CORS policy remains a limitation. |
| PyJWT | 1.7.1 → 2.10.1 | Update signing/verification API: encoded tokens are strings, subject is a string, verification explicitly allows HS256. API returns numeric user IDs after verification. Historical numeric-subject tokens may be rejected; secret rotation already requires token invalidation. |
| PyYAML | 5.3.1 → 6.0.2 | Python 3.12 wheel installation; safe YAML loading retained. |
| SQLAlchemy | 1.3.16 → 1.4.54 | Python 3.12-compatible release retaining the legacy ORM/metadata API. Avoid 2.x migration; deprecation warnings remain. Structured URL construction preserves credential characters. |
| PostgreSQL driver | psycopg2 2.8.5 → psycopg2-binary 2.9.10 | Wheel installation without a local C/PostgreSQL build toolchain for this development image. |
| WTForms | 2.3.1 → 2.3.3 | Retain 2.x API with patch update; no form redesign. |
| Optional polling | Eventlet 0.25.2 → 0.40.3; Socket.IO 4.5.1 → 4.6.1; Engine.IO 3.12.1 → 3.14.2 | Python runtime compatibility while preserving Socket.IO 4 / Engine.IO 3 client protocol generation. Local handshake verified. |
| Docker | Ubuntu 18.04 system Python → python:3.12-slim | Reproducible Python target and wheel-based installation; HTTP service remains the default command. |

Unused eager model import removed from `private/api/user.py`. ML source remains unchanged; no model behavior or training claim is made. The optional research stack is not installed or validated. Transitive dependencies resolve from the package index and are not fully locked; this is not a supply-chain audit.

## Checks actually run

| Check | Observed result |
|---|---|
| Isolated Python 3.12.6 venv: `pip install -r requirements.txt` | Passed |
| `pip install -r requirements-polling.txt` | Passed |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | 13 passed locally |
| `python -m pip check` | Passed |
| `python -m compileall -q main.py private tests` | Passed |
| `docker build -t virus-hack:portfolio-check .` | Passed using Docker Desktop 29.2.1 |
| Same 13 new tests inside image | Passed |
| `python commands.py create_db` in image with isolated PostgreSQL 16 container | Passed after FlaskGroup compatibility fix |
| Original `python test.py` against newly created schema | **Failed:** `ForeignKeyViolation`; inserts a university recommendation referencing user 1 before inserting the user. Original test preserved. |
| Actual `polls.py` process, GET `/socket.io/?EIO=3&transport=polling` | HTTP 200 handshake with session ID; process stopped afterward |
| Historical YAML credential-value comparison against current tracked files | No old values found; values never printed |
| Private-key marker scan of current tracked files | No matches |
| README five-H2 order and `git diff --check` | Passed |

Database and test network were created for this check and removed afterward. No existing user database was modified. This validates schema creation, not full DB route behavior. Poll submission/publishing persistence, authorization coverage, complete role/user seeding, optional ML experiments, and an end-to-end frontend flow remain untested. No benchmark was performed.
