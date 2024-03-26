FROM python:3.10

WORKDIR /usr/src/app

COPY . .

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt

# EXPOSE 8000:8000

# CMD ["python","manage.py","runserver"]


