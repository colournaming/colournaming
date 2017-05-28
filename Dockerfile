FROM python:3.6
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY colournaming /app
VOLUME /app
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run"]
