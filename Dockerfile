FROM nvidia/cuda:12.9.1-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    python3.12 -m ensurepip --upgrade && \
    python3.12 -m pip install --upgrade pip

# Install vllm (>= 0.18.0)
ENV VLLM_USE_TORCH_BACKEND=auto
RUN python3.12 -m pip install --no-cache-dir "vllm>=0.18.0"

# Install vllm-omni for TTS support
RUN python3.12 -m pip install --no-cache-dir git+https://github.com/vllm-project/vllm-omni.git

# Create models directory
RUN mkdir -p /models

WORKDIR /app

EXPOSE 4576

CMD ["bash", "-c", "if [ -n \"$HF_TOKEN\" ]; then huggingface-cli login --token $HF_TOKEN; fi && vllm serve mistralai/Voxtral-4B-TTS-2603 --omni --host 0.0.0.0 --port 4576"]
