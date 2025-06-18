

FROM python:3.13-slim



COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


COPY . /app


WORKDIR /app


RUN uv sync 


CMD ["./.venv/bin/python", "main.py"]