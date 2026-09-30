FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PYTHONUNBUFFERED=1

# Accept UID and GID as build arguments (default to 1000 if not provided)
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN mkdir /app
RUN addgroup --gid ${GROUP_ID} colournaming && \
    adduser --disabled-password --gecos '' --uid ${USER_ID} --gid ${GROUP_ID} colournaming && \
    chown -R colournaming:colournaming /app && \
    touch /app/colournaming.log && \
    chmod 666 /app/colournaming.log
USER colournaming
ENV FLASK_APP=/app/app.py
COPY pyproject.toml /app
COPY uv.lock /app
COPY colournaming /app/colournaming
COPY app.py /app
COPY tests /app
COPY docker.cfg /app
WORKDIR /app
RUN uv python install 3.13 && uv sync --locked
ENTRYPOINT ["uv", "run", "flask"]
CMD ["run"]
