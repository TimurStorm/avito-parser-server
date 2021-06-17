# установка базового образа (host OS)
FROM python:3.8
# установка рабочей директории в контейнере
WORKDIR /usr/src/bot
# копирование файла зависимостей в рабочую директорию
# установка зависимостей
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VERBOSITY -1

RUN apt update
RUN apt install netcat -y
RUN apt install -y gettext libgettextpo-dev

RUN pip install --upgrade pip
RUN pip install aiovk
RUN pip install asyncio
RUN pip install python-dotenv
RUN pip install sanic

# копирование содержимого локальной директории src в рабочую директорию
COPY . .
# команда, выполняемая при запуске контейнера
CMD [ "python", "./server.py" ]