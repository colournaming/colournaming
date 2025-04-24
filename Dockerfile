FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN adduser --disabled-password -gecos '' colournaming && \
    chown -R colournaming /app && \
    touch /app/colournaming.log && \
    chmod 666 /app/colournaming.log
USER colournaming
ENV FLASK_APP /app/app.py
COPY pyproject.toml /app
COPY uv.lock /app
COPY colournaming /app
COPY colournaming /app
COPY app.py /app
COPY tests /app
COPY docker.cfg /app
WORKDIR /app
RUN uv sync --locked
ENTRYPOINT ["uv", "run", "flask"]
CMD ["run"]
