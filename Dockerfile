FROM python:3.11-alpine

RUN pip install flask requests

WORKDIR /app
COPY app.py .

EXPOSE 9094

CMD ["python", "app.py"]
