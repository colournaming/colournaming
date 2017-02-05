FROM python:3.6
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
ENV FLASK_APP /app/app.py
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run"]