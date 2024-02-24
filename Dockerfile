FROM python:3.10.8-slim
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT ["python3", "wsgi.py"]