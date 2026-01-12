FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN useradd -m -u 1000 safeshare && \
    mkdir -p /app /tmp/safeshare_temp && \
    chown -R safeshare:safeshare /app /tmp/safeshare_temp

WORKDIR /app

COPY --chown=safeshare:safeshare . .

USER safeshare

ENV PYTHONUNBUFFERED=1
ENV TEMP_DIR=/tmp/safeshare_temp

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "main.py"]