FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/db.py .

CMD ["streamlit", "run", "db.py", "--server.address=0.0.0.0"]