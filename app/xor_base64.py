import base64
import itertools
#XOR related functions
charset = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r')
charset_base64 = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=')

def xor(plain_text, key): 
    
    # xor plain_text with key 
    pt = plain_text 
    len_key = len(key) 
    encoded = [] 
      
    for i in range(0, len(pt)): 
        encoded.append(pt[i] ^ key[i % len_key])
    return bytes(encoded)

def smart_xorkeys(input_xored, test_key_len, charset):
#key_len in bytes
  possible = [set(range(256)) for _ in range(test_key_len)]
  for i, char in enumerate(input_xored):
    new = set()
    for possible_key in possible[i % test_key_len]:
      decoded = char ^ possible_key
      if decoded in charset:
        new.add(possible_key)
    possible[i % test_key_len] = new

  return list(itertools.product(*possible))

def brute_xorkeys(input_xored, test_key_len):
  possible = [set(range(256)) for _ in range(test_key_len)]
  return list(itertools.product(*possible))

def smart_xorkeys_top_printable(input_xored, test_key_len, check_top, charset):
#key_len in bytes
  possible = [set(range(256)) for _ in range(test_key_len)]
  key_success_count = [[0]*256 for _ in range(test_key_len)]

  for i, char in enumerate(input_xored):

    for j, possible_key in enumerate(possible[i % test_key_len]):
      decoded = char ^ possible_key
      if decoded in charset:
        key_success_count[i % test_key_len][j] += 1

  top_list = []
  srt = []
  for c in range(test_key_len):
    srt.append(sorted(range(256), key=lambda k: key_success_count[c][k], reverse = True))
    top_list.append(srt[-1][:check_top])

  return list(itertools.product(*top_list))

#base64 related functions
def isBase64(sb):
  try:
    if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
    elif isinstance(sb, bytes):
            sb_bytes = sb
    else:
            raise ValueError("Argument must be string or bytes")
    return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
  except Exception:
    return False

def base64_recursive_decode(encoded):
  decoded = encoded
  while(isBase64(decoded)):
    decoded = base64.b64decode(decoded)

  return decoded