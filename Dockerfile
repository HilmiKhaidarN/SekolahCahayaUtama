FROM python:3.9-slim

WORKDIR /app

# Install dependensi langsung karena hanya butuh Flask
RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]