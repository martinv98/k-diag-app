FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

VOLUME /app/instance

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["run.py"]