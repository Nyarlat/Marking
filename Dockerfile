# Базовый образ с CUDA 11.8 и cuDNN 8
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Установка базовых утилит и Python
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118

CMD ["python3"]
