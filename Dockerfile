FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt ./app/main.py ./app/guess_xor_length.py ./app/recipe.py ./app/check_english.py ./app/xor_base64.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
