FROM alpine

RUN apk add --no-cache python3 py3-pip

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

COPY /app/. /app/
COPY /Storage/* /app/Storage/
COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --break-system-packages --upgrade pip && pip3 install --break-system-packages --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

CMD ["python3", "maasser_main.py"]
