FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
#FROM python:3.7-slim

COPY requirements.txt ./app/main.py ./app/guess_xor_length.py ./app/recipe.py ./app/check_english.py ./app/xor_base64.py ./app/words.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]
