FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache bash git openssh

COPY main.py /main.py
CMD [ "python", "/main.py" ]
