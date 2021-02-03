FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/news-parser/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY /src /news-parser/src

CMD ["python", "src/hello.py"]
