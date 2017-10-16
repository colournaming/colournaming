FROM python:3.6
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN pip install -q -r /tmp/requirements.txt && pip install -q gunicorn
COPY colournaming /app/colournaming
COPY app.py /app
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run"]
