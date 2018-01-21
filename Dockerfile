FROM python:3.6.4
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/origami
WORKDIR /opt/origami

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
