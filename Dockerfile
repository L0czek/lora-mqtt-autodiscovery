FROM python:alpine

WORKDIR /app
COPY ./ ./ 

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python3", "-u", "./bin/server.py"]
