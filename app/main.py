
from fastapi import FastAPI
import recipe
import base64
from xor_base64 import xor, base64_recursive_decode
from urllib.parse import unquote, quote

charset = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r')
charset_base64 = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
