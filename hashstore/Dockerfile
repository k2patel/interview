FROM python:3

ENV LANG C.UTF-8


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install flask
RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py
VOLUME ["/usr/src/app/data"]

EXPOSE 5000
CMD ["/usr/local/bin/flask", "run", "--host", "0.0.0.0"]
