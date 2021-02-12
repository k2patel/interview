FROM python:3.9
WORKDIR /app
RUN mkdir /app/test_data
COPY solution.py .
COPY test_data/01-input test_data/ 
CMD ["python3", "solution.py"]
