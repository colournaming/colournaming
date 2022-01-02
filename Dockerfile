FROM python:3.8
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN pip install pip==21.0.1 && pip install wheel pip-tools
RUN pip-sync /tmp/requirements.txt
COPY colournaming /app/colournaming
COPY app.py /app
COPY tests /app/tests
COPY docker.cfg /app
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run"]
