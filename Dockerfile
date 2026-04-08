FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1

CMD ["python", "-m", "uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860", "--timeout-keep-alive", "75"]
