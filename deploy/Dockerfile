ARG PYTHON_VERSION=3.10

ARG APP_NAME=app
ARG APP_PATH=/opt/backend
ARG FULL_APP_PATH=$APP_PATH/$APP_NAME

FROM python:$PYTHON_VERSION as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:$PYTHON_VERSION-alpine

ARG APP_NAME
ARG APP_PATH
ARG FULL_APP_PATH

WORKDIR $APP_PATH
COPY --from=requirements-stage /tmp/requirements.txt $APP_PATH/requirements.txt
RUN pip install --no-cache-dir --upgrade -r $APP_PATH/requirements.txt
COPY ./$APP_NAME $FULL_APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
ENV \
    PORT=8000 \
    APP_NAME=$APP_NAME \
    PACKAGE="$APP_NAME.main:app"

COPY ./deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "$PACKAGE", "--host", "0.0.0.0", "--port", "$PORT"]

