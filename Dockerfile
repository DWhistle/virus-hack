FROM ubuntu:18.04
COPY . /app
WORKDIR /app
RUN apt update && \
    apt install -y --fix-missing build-essential && \
    apt install -y --fix-missing python3 && \
    apt install -y --fix-missing python3-pip
RUN python3 -m pip install --upgrade --force pip && \
     pip install --upgrade cython && \
     python3 -m pip install -r requirements.txt
CMD python3 ./main.py