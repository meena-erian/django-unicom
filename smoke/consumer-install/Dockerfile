FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY dist /wheels

FROM base AS runtime

ARG UNICOM_INSTALL_SOURCE=local-wheel
ARG UNICOM_INSTALL_VERSION=

RUN if [ "$UNICOM_INSTALL_SOURCE" = "local-wheel" ]; then \
        pip install --no-cache-dir /wheels/*.whl; \
    elif [ "$UNICOM_INSTALL_SOURCE" = "pypi" ] && [ -n "$UNICOM_INSTALL_VERSION" ]; then \
        pip install --no-cache-dir "django-unicom==$UNICOM_INSTALL_VERSION"; \
    elif [ "$UNICOM_INSTALL_SOURCE" = "pypi" ]; then \
        pip install --no-cache-dir django-unicom; \
    else \
        echo "Unsupported UNICOM_INSTALL_SOURCE: $UNICOM_INSTALL_SOURCE" >&2; \
        exit 1; \
    fi

COPY smoke/consumer-install/app /app

EXPOSE 8000
