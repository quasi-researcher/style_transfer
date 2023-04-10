FROM pytorch/torchserve

WORKDIR /model_server
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["torchserve", "--start", "--model-store", "/model_server", "--models", "fmnist=/model_server/fashion_mnist.mar", "--ts-config", "/model_server/torch_config"]