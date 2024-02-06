# syntax=docker/dockerfile:1
FROM python:3.10.12
WORKDIR /animaldetect
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python" ,"./app.py" ]
