# syntax=docker/dockerfile:1

FROM python:3.11.9-slim
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install tensorflow==2.16.1 -f https://tf.kmtea.eu/whl/stable.html
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]