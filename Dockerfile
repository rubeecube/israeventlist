FROM alpine

RUN apk add --update --no-cache \
    python3 \
    py3-pip

RUN apk add --update --no-cache --virtual \
    .tmp-build-deps \
    libc-dev \
    linux-headers

RUN apk add --update \
  build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  postgresql-client \
  postgresql-dev \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev

COPY /app/. /app/
#COPY /Storage/* /app/Storage/
COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --break-system-packages --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

CMD ["python3", "maasser_main.py"]
