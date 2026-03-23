# Consumer Install Smoke Test

This stack verifies the documented consumer path: install `django-unicom` as a library inside a minimal Django project instead of relying on the workspace submodule layout.

By default it installs from the local wheel in `dist/`, which keeps the test reproducible inside this repo.

```bash
cd smoke/consumer-install
docker compose up --build --abort-on-container-exit smoke
```

To test the latest published package from PyPI:

```bash
cd smoke/consumer-install
UNICOM_INSTALL_SOURCE=pypi docker compose up --build --abort-on-container-exit smoke
```

To test a pinned PyPI version:

```bash
cd smoke/consumer-install
UNICOM_INSTALL_SOURCE=pypi UNICOM_INSTALL_VERSION=25.4.1 docker compose up --build --abort-on-container-exit smoke
```

To investigate installation manually inside a plain container without the package preinstalled:

```bash
cd smoke/consumer-install
docker compose up -d --build debug
docker compose exec debug sh
```

Then inside the container:

```bash
python -c "import socket; print(socket.gethostbyname('pypi.org'))"
pip install django-unicom
pip install /wheels/*.whl
```

What it checks:

- Django can start with `unicom` installed as a package
- Migrations run in a fresh PostgreSQL database
- `unicom` URLs are mounted and the WebChat demo page renders
- A minimal active WebChat channel can receive a message
- Chats and messages can be fetched back over HTTP

Notes:

- The PyPI package name is `django-unicom`.
- This smoke stack uses PostgreSQL because `unicom` migrations rely on PostgreSQL-specific fields such as `ArrayField`.
- There is no special official PyPI `lts` channel here. If you want an LTS-style test target, pin the version you consider your supported baseline with `UNICOM_INSTALL_VERSION`.
- `local-wheel` expects a wheel to exist in [`dist`](/home/menas/rf2/unicom/dist).
