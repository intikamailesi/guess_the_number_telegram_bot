FROM python:3.8.0-slim-buster
COPY . .
RUN pip install -r requirements.txt
ENV BOT_TOKEN place_your_uber_sequre_token_here
CMD ["python", "./run.py"]

