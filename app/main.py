
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

@app.get("/brute/")
def brute_decode(to_decode, maxlen, results_to_show):

    to_decode = unquote(to_decode)
    to_decode = bytes(to_decode, 'ascii')

    decoded = recipe.xor_brute(to_decode, int(maxlen), int(results_to_show))
    joint_list = []
    output_dict = {}

    for i in range(len(decoded)):
        joint_list += decoded[i]

    added = 1
    for i in range(len(joint_list)):
        if joint_list[i][-1] in output_dict.values():
            continue

        output_dict[str(added) + ") Key "] = (joint_list[i][1]).decode()
        output_dict[str(added) + ") Decoded "] = joint_list[i][-1]

        if added == int(results_to_show):
            break

        added += 1

    return output_dict
