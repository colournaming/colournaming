FROM python:3.6
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN pip install pip==21.0.1
RUN pip install -q -r /tmp/requirements.txt && pip install -q gunicorn
COPY colournaming /app/colournaming
COPY app.py /app
COPY tests /app/tests
COPY docker.cfg /app
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run"]
