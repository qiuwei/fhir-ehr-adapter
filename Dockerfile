FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ .

COPY wait-for-it.sh wait-for-it.sh

EXPOSE 3004
CMD [ "python", "receive.py" ]
