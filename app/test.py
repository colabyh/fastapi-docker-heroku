import recipe
import base64
from xor_base64 import xor, base64_recursive_decode
from urllib.parse import unquote, quote

charset = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r')
charset_base64 = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=')

ping_string = b'''
Pinging google.com [2404:6800:4003:c00::8b] with 32 bytes of data:
Reply from 2404:6800:4003:c00::8b: time=15ms
Reply from 2404:6800:4003:c00::8b: time=36ms
Reply from 2404:6800:4003:c00::8b: time=9ms
Reply from 2404:6800:4003:c00::8b: time=6ms

Ping statistics for 2404:6800:4003:c00::8b:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 6ms, Maximum = 36ms, Average = 16ms'''

# print(recipe.xor_fast(ping_string, 4, charset))

# print(recipe.xor_guess_keylen(ping_string, charset))

#encoded = xor(ping_string, b'TEST')
# print(recipe.auto_deobf(encoded, 5, 4))

# encoded = xor(base64.b64encode(ping_string), b'TEST')
# print(recipe.auto_deobf(encoded, 5, 4))

# print(recipe.xor_fast(encoded, 4, charset_base64))

# encoded = xor(ping_string, b'T')

# decoded = recipe.xor_brute(encoded, 1, 1)
# #print(recipe.xor_brute(encoded, 1, 1))

# print(decoded[0][-1])

def fastxor(to_decode, keylen, choose_charset, results_to_show):

    to_decode = unquote(to_decode)
    to_decode = base64_recursive_decode(to_decode)

    if int(choose_charset) == 0:
        decoded = recipe.xor_fast(to_decode, int(keylen), charset, int(results_to_show))

    if int(choose_charset) == 1:
        decoded = recipe.xor_fast(to_decode, int(keylen), charset_base64, int(results_to_show))
    
    joint_list = []
    output_dict = {}

    for i in range(len(decoded)):
        joint_list += decoded[i]

    added = 1
    for i in range(len(joint_list)):
        if joint_list[i][-1] in output_dict.values():
            continue

        output_dict[str(added) + ") Key "] = (joint_list[i][1]).decode()
        output_dict[str(added) + ") Decoded "] = quote(joint_list[i][-1])

        if added == int(results_to_show):
            break

        added += 1

    return output_dict

#to_decode = "AQI/IQ53PyEOPBE6NndqOjYCBiENd2ogHQMgLRoBEmQbLwpgGQESYhoBEiMZPyM+GQESYhsvOz0MFhFnNR0BOx0BHi0dAhlhMAIFLh0CajkdAgE8MAIWYhcpGTg3AithHQIJLTZ3YzMZLwIjGgE8ZhsBEiMbLwIjGQEeYg0/EiMbLzxgDS88MzACPyAOEWMsGhJiLhcpGTg3AithHQIJLTZ3YzMZLwIjGgE8ZhsBEiMbLwIjGQEeYg0/EiMbLzxgDS88MzACPyAOEWMuGihiLhcpGTg3AithHQIJLTZ3YzMZLwIjGgE8ZhsBEiMbLwIjGQEeYg0/EiMbLzxgDS88MzACPyAOEWNhNh0eHwEoBSM2DTgzDisZIjYWEi0aARJkGy8KYBkBEmIaARIjGT8jPhkBEmIbLzs9GywRZDUSYjgEEQkgNzI8HwECPyEOPBEuMAIVZDUdHWQ1Eh0uHQIJIjcsEi0aARJkGy8KYBkBEmIaARIjGT8jPhkBEmIbLzs9"


#print(fastxor(to_decode, 4, 1, 200))

# print("\n\n\n")
# to_decode = "MAIFLjAGEWQOHR1kHQ0BODd2AjMwAgUuMARuaQ%3D%3D"
# to_decode = unquote(to_decode)
# to_decode = base64_recursive_decode(to_decode)

# print(recipe.xor_fast(to_decode, 4, charset_base64))
# print(to_decode)

def magic(to_decode, keylen, results_to_show, early_stop):
    #auto_deobf(string_to_decode, maxlen, ret_num = 1, early_stop_count = 3, early_stop_len = 3)
    to_decode = unquote(to_decode)
    # to_decode = base64_recursive_decode(to_decode)

    print(to_decode)
    #to_decode = bytes(to_decode, 'ascii')
    decoded = recipe.auto_deobf(to_decode, int(keylen), int(results_to_show), int(early_stop), int(early_stop))
 
    #decoded = recipe.auto_deobf(to_decode, 3, 20, 3, 3)
    #return len(decoded)
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
            print("pass")

        if added == int(results_to_show):
            break

        added += 1

    return output_dict

#to_decode = b'4673bb7f41b13d78837479ba467da74658a14c6d814e4baf444e8d7447b14c6d814e4ba45f4c864152b24470825e4bb969388e7e688f5b3a83643ff86842997e41a64366925a5bb941649a396e8b7a7b916358a24663fd3d6f805c79844e7aba5752a37c46a65f3eac4e7db94067926541a1383aad455bbb46608260539b627fab4a3fa64149a77450a5487b84607abf5773bf7c53905b3aa94e65bd6c648a63468b7d62ac5558a74663fd7a68a56e79836044b168528a3d68b1627fac4562f84149b86768fa617f83643ff86842997e41a64f7caa4a33bd6c5d9e3941a17a7ba93e40a06c389e7841a17a7baa3f7ea46849a77e41a5477aaa604cbd54389d7c468b7d63a95558a56c5dfd616f8b627983606ea35452af7c468b7d7dab6066fa54529a6141a1383aad455bbb46649e7a53a5613a844e65b9546786616f8b6279836040b8694da07d689f447b844e7aa76c529a646e8f407b844e7aa16c529a6068806166ab6465bb4667bc3c53fa347aaa6465bb4667a03c68fa477a83647db969388e7e688f5b3a84607ab26f38fc7c438b4c6d814e4baf444e8d7a438b4c6d814e4bba4449896a438b4c6d845e4baf4449896a49af7d40814e4baf4449896a479c4c7f85643eb24160993b5c8f4b7aac3f4cbd%0A%0A'
to_decode = '4673bb7f41b13d78837479ba467da74658a14c6d814e4baf444e8d7447b14c6d814e4ba45f4c864152b24470825e4bb969388e7e688f5b3a83643ff86842997e41a64366925a5bb941649a396e8b7a7b916358a24663fd3d6f805c79844e7aba5752a37c46a65f3eac4e7db94067926541a1383aad455bbb46608260539b627fab4a3fa64149a77450a5487b84607abf5773bf7c53905b3aa94e65bd6c648a63468b7d62ac5558a74663fd7a68a56e79836044b168528a3d68b1627fac4562f84149b86768fa617f83643ff86842997e41a64f7caa4a33bd6c5d9e3941a17a7ba93e40a06c389e7841a17a7baa3f7ea46849a77e41a5477aaa604cbd54389d7c468b7d63a95558a56c5dfd616f8b627983606ea35452af7c468b7d7dab6066fa54529a6141a1383aad455bbb46649e7a53a5613a844e65b9546786616f8b6279836040b8694da07d689f447b844e7aa76c529a646e8f407b844e7aa16c529a6068806166ab6465bb4667bc3c53fa347aaa6465bb4667a03c68fa477a83647db969388e7e688f5b3a84607ab26f38fc7c438b4c6d814e4baf444e8d7a438b4c6d814e4bba4449896a438b4c6d845e4baf4449896a49af7d40814e4baf4449896a479c4c7f85643eb24160993b5c8f4b7aac3f4cbd'
print(magic(to_decode, 3, 20, 3))
#print(recipe.auto_deobf(to_decode, 3, 20, 3, 3))

#4673bb7f41b13d78837479ba467da74658a14c6d814e4baf444e8d7447b14c6d814e4ba45f4c864152b24470825e4bb969388e7e688f5b3a83643ff86842997e41a64366925a5bb941649a396e8b7a7b916358a24663fd3d6f805c79844e7aba5752a37c46a65f3eac4e7db94067926541a1383aad455bbb46608260539b627fab4a3fa64149a77450a5487b84607abf5773bf7c53905b3aa94e65bd6c648a63468b7d62ac5558a74663fd7a68a56e79836044b168528a3d68b1627fac4562f84149b86768fa617f83643ff86842997e41a64f7caa4a33bd6c5d9e3941a17a7ba93e40a06c389e7841a17a7baa3f7ea46849a77e41a5477aaa604cbd54389d7c468b7d63a95558a56c5dfd616f8b627983606ea35452af7c468b7d7dab6066fa54529a6141a1383aad455bbb46649e7a53a5613a844e65b9546786616f8b6279836040b8694da07d689f447b844e7aa76c529a646e8f407b844e7aa16c529a6068806166ab6465bb4667bc3c53fa347aaa6465bb4667a03c68fa477a83647db969388e7e688f5b3a84607ab26f38fc7c438b4c6d814e4baf444e8d7a438b4c6d814e4bba4449896a438b4c6d845e4baf4449896a49af7d40814e4baf4449896a479c4c7f85643eb24160993b5c8f4b7aac3f4cbd