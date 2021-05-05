from fastapi import FastAPI
import recipe
import base64
from xor_base64 import xor, base64_recursive_decode
from urllib.parse import unquote, quote

from pydantic import BaseModel

charset = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r')
charset_base64 = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=')

app = FastAPI()

def create_output(decoded):
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/brute/")
def brute_decode(to_decode, maxlen, results_to_show, base64encoded):

    to_decode = unquote(to_decode)
    to_decode = bytes(to_decode, 'ascii')

    if (int(base64encoded)==1):
        to_decode = base64.b64decode(to_decode)

    decoded = recipe.xor_brute(to_decode, int(maxlen), int(results_to_show))
    joint_list = []
    output_dict = {}

    for i in range(len(decoded)):
        joint_list += decoded[i]

    added = 1
    for i in range(len(joint_list)):
        try:
            printable = ""
            
            for j in joint_list[i][-1]:
                if j in charset:
                    printable += chr(j)
                else:
                   printable += "."

            if (printable) in output_dict.values():
                continue

            output_dict[str(added) + ") Key "] = str(joint_list[i][1])
            output_dict[str(added) + ") Decoded "] = printable
        except:
            pass

        if added == int(results_to_show):
            break

        added += 1

    return output_dict

@app.get("/guess_xorlen/")
def guess_xorlen(to_decode, results_to_show, base64encoded):

    to_decode = unquote(to_decode)
    to_decode = bytes(to_decode, 'ascii')

    if (int(base64encoded)==1):
        to_decode = base64.b64decode(to_decode)

    to_decode = base64_recursive_decode(to_decode)

    decoded = recipe.xor_guess_keylen(to_decode, charset, int(results_to_show))

    joint_list = []
    output_dict = {}

    if decoded is None:
        return output_dict

    for i in range(len(decoded)):
        joint_list += decoded[i]

    added = 1
    for i in range(len(joint_list)):
        try:
            printable = ""
            
            for j in joint_list[i][-1]:
                if j in charset:
                    printable += chr(j)
                else:
                   printable += "."

            if (printable) in output_dict.values():
                continue

            output_dict[str(added) + ") Key "] = str(joint_list[i][1])
            output_dict[str(added) + ") Decoded "] = printable
        except:
            pass

        if added == int(results_to_show):
            break

        added += 1

    return output_dict

@app.get("/fastxor/")
def fastxor(to_decode, keylen, choose_charset, results_to_show, base64encoded):

    to_decode = unquote(to_decode)
    to_decode = bytes(to_decode, 'ascii')
    #to_decode = base64_recursive_decode(to_decode)

    if (int(base64encoded)==1):
        to_decode = base64.b64decode(to_decode)

    # if int(choose_charset) == 0:
    #     decoded = recipe.xor_fast(to_decode, int(keylen), charset, int(results_to_show))

    # if int(choose_charset) == 1:
    #     decoded = recipe.xor_fast(to_decode, int(keylen), charset_base64, int(results_to_show))
    
    decoded = recipe.xor_fast(to_decode, int(keylen), int(choose_charset), int(results_to_show))

    joint_list = []
    output_dict = {}

    for i in range(len(decoded)):
        joint_list += decoded[i]

    added = 1
    for i in range(len(joint_list)):
        try:
            printable = ""
            
            for j in joint_list[i][-1]:
                if j in charset:
                    printable += chr(j)
                else:
                   printable += "."

            if (printable) in output_dict.values():
                continue

            output_dict[str(added) + ") Key "] = str(joint_list[i][1])
            output_dict[str(added) + ") Decoded "] = printable
        except:
            pass

        if added == int(results_to_show):
            break

        added += 1

    return output_dict

@app.get("/magic/")
def magic(to_decode, keylen, results_to_show, early_stop, base64encoded):
    
    to_decode = unquote(to_decode)
    to_decode = bytes(to_decode, 'ascii')

    if (int(base64encoded)==1):
        to_decode = base64.b64decode(to_decode)

    decoded = recipe.auto_deobf(to_decode, int(keylen), int(results_to_show), int(early_stop), int(early_stop))

    joint_list = []
    output_dict = {}

    for i in range(len(decoded)):
        joint_list += decoded[i]

    added = 1
    for i in range(len(joint_list)):

        try:
            printable = ""
            
            for j in joint_list[i][-1]:
                if j in charset:
                    printable += chr(j)
                else:
                   printable += "."

            if (printable) in output_dict.values():
                continue

            output_dict[str(added) + ") Key "] = str(joint_list[i][1])
            output_dict[str(added) + ") Decoded "] = printable
        except:
            pass

        if added == int(results_to_show):
            break

        added += 1

    return output_dict