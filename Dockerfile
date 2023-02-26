FROM python:3.8

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn app:app --host 0.0.0.0 --port 8002 

