# temp stage
FROM python:alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# final stage
FROM python:alpine

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH="/opt/venv/bin:$PATH"

COPY de421.bsp .
COPY moon_new.py .
COPY http_server.py .
CMD ["python", "http_server.py"]
