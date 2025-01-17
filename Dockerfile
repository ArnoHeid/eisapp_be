FROM python:alpine3.7
COPY app /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]