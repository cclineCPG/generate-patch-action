FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]
