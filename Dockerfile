FROM alpine

RUN apk add --no-cache python3 py3-pip

COPY /app/. /app/
COPY /Storage/* /app/Storage/
COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --break-system-packages --upgrade pip && pip3 install --break-system-packages --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

CMD ["python3", "maasser_main.py"]
