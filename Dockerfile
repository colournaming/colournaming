FROM python:3.8
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN pip install pip==21.0.1 && pip install wheel pip-tools
RUN pip-sync /tmp/requirements.txt
COPY colournaming /app/colournaming
COPY app.py /app
COPY tests /app/tests
COPY docker.cfg /app
RUN useradd colournaming && \
    chown -R colournaming /app/colournaming /app/tests && \
    chown colournaming /app/docker.cfg /app/app.py && \
    find /app/colournaming -type d -exec chmod 555 {} \; && \
    find /app/tests -type d -exec chmod 555 {} \; && \
    chmod 440 /app/docker.cfg /app/app.py
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
USER colournaming
CMD ["run"]
