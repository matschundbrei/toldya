FROM python:3-alpine

# Pillow dependencies
RUN apk add --no-cache python3 \
                       build-base \
                       python3-dev \
                       # wget dependency
                       openssl \
                       # dev dependencies
                       git \
                       bash \
                       sudo \
                       py3-pip \
                       # actual pillow deps
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev

WORKDIR /opt/toldya

COPY . ./

ENV VIRTUAL_ENV=/opt/toldya/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 8080

ENV FLASK_APP toldya
# run it
CMD ["./entrypoint.sh"]
