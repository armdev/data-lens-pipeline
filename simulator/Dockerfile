FROM python:3.9-slim

RUN pip install psycopg2-binary

WORKDIR /app
COPY simulator.py .

CMD ["python", "simulator.py"]
