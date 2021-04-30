# установка базового образа (host OS)
FROM python:3.8
# установка рабочей директории в контейнере
WORKDIR /usr/src/app
# копирование файла зависимостей в рабочую директорию
# установка зависимостей
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VERBOSITY -1

RUN apt update
RUN apt install netcat -y
RUN apt install -y gettext libgettextpo-dev

RUN pip install --upgrade pip
RUN pip install poetry==1.0.10
COPY pyproject.toml /usr/src/app/pyproject.toml
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt
# копирование содержимого локальной директории src в рабочую директорию
COPY main/ .
COPY user/ .
# команда, выполняемая при запуске контейнера
CMD [ "python", "./server.py" ]