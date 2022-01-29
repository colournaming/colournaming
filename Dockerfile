FROM python:3.8
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN pip install pip==21.0.1 && pip install wheel pip-tools
RUN pip-sync /tmp/requirements.txt
COPY colournaming /app/colournaming
COPY app.py /app
COPY tests /app/tests
COPY docker.cfg /app
RUN adduser --disabled-password -gecos '' colournaming && \
    chown -R colournaming /app && \
    chown colournaming /app/docker.cfg /app/app.py && \
    find /app -type d -exec chmod 555 {} \; && \
    find /app -type f -exec chmod 444 {} \; && \
    touch /app/colournaming.log && \
    chmod 666 /app/colournaming.log
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
USER colournaming
CMD ["run"]
