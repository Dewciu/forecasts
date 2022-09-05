FROM python:3.10.5

WORKDIR /forecasts

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src

CMD ["python", "src/main.py", "systems", "forecasts", "-c"]