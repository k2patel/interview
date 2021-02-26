FROM python:3.9

WORKDIR /app
COPY solution.py .
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "solution.py"]
