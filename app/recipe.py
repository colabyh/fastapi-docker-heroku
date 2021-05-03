import guess_xor_length
import xor_base64
import check_english
import binascii

charset = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r')
charset_base64 = set(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=')

def xor_guess_keylen(string_to_decode, charset, ret_num = 1):
  """
  first tries to guess the key length
  works best if XOR output is English
  """
  string_to_decode = xor_base64.base64_recursive_decode(string_to_decode)
  keylen, fitness = guess_xor_length.guess_key_length(string_to_decode)
  #print(keylen, fitness)
  if fitness < 1:
    print("Cannot guess key length")
    return

  keys = [bytearray(x) for x in xor_base64.smart_xorkeys(string_to_decode, keylen, charset)]
  outputs = [xor_base64.xor(string_to_decode, key) for key in keys]
  top_count_output = []
  top_count = 0

  longest_output = []
  longest = 0

  for key, output in zip(keys, outputs):
    output = xor_base64.base64_recursive_decode(output)
    eng_count, long_count = check_english.get_eng_counts(output)

    if eng_count > top_count:
      top_count = eng_count

    if long_count > longest:
      longest = long_count

    top_count_output.append((eng_count, key, output))
    longest_output.append((long_count, key, output))


  if len(top_count_output) > 1:
    top_count_output.sort(reverse = True)

  if len(longest_output) > 1:
    longest_output.sort(reverse = True)

  return longest_output[:min(ret_num,len(longest_output))], \
  top_count_output[:min(ret_num,len(top_count_output))]

def xor_fast(string_to_decode, keylen, charset_fast, ret_num = 1):
  """
  knowledge of keylen and decoded char set
  """
  keys = [bytearray(x) for x in xor_base64.smart_xorkeys(string_to_decode, keylen, charset_fast)]
  outputs = [xor_base64.xor(string_to_decode, key) for key in keys]
  top_count_output = []
  top_count = 0

  longest_output = []
  longest = 0

  for key, output in zip(keys, outputs):
    output = xor_base64.base64_recursive_decode(output)
    eng_count, long_count = check_english.get_eng_counts(output)

    if eng_count > top_count:
      top_count = eng_count

    if long_count > longest:
      longest = long_count

    top_count_output.append((eng_count, key, output))
    longest_output.append((long_count, key, output))


  if len(top_count_output) > 1:
    top_count_output.sort(reverse = True)

  if len(longest_output) > 1:
    longest_output.sort(reverse = True)

  return longest_output[:min(ret_num,len(longest_output))], \
  top_count_output[:min(ret_num,len(top_count_output))]

def xor_brute(string_to_decode, maxkeylen, ret_num = 20):
  """
  brute force for key length smaller than maxkeylen
  """
  top_count_output = []
  top_count = 0

  longest_output = []
  longest = 0
  for keylen in range(1, maxkeylen+1):
    keys = [bytearray(x) for x in xor_base64.brute_xorkeys(string_to_decode, keylen)]
    outputs = [xor_base64.xor(string_to_decode, key) for key in keys]

    for key, output in zip(keys, outputs):
      
      eng_count, long_count = check_english.get_eng_counts(output)

      if eng_count > top_count:
        top_count = eng_count

      if long_count > longest:
        longest = long_count
        
      top_count_output.append((eng_count, key, output))
      longest_output.append((long_count, key, output))

  #  if top_count > early_stop_count or longest > early_stop_len:
  if len(top_count_output) > 1:
    top_count_output.sort(reverse = True)

  if len(longest_output) > 1:
    longest_output.sort(reverse = True)

  print("Stop at brute force")
  return longest_output[:min(ret_num,len(longest_output))], \
  top_count_output[:min(ret_num,len(top_count_output))]

def auto_deobf(string_to_decode, maxlen, ret_num = 1, early_stop_count = 3, early_stop_len = 3):
  """
  converts from HEX to ascii
  tries a combination of base64 and XOR decoding
  bruteforce keylen to maxlen
  works well if XOR output is base64 encoded
  returns top ret_num matches
  """

  try:
    int(string_to_decode, 16)
    string_to_decode = binascii.unhexlify(string_to_decode)
  except:
    pass

  print("Start base64")
  string_to_decode = xor_base64.base64_recursive_decode(string_to_decode)
  
  top_count_output = []
  top_count = 0

  longest_output = []
  longest = 0

  eng_count, long_count = check_english.get_eng_counts(string_to_decode)
  top_count_output.append((eng_count, b'base64', string_to_decode))
  longest_output.append((long_count, b'base64', string_to_decode))

  if eng_count > top_count:
    top_count = eng_count

  if long_count > longest:
    longest = long_count

  if top_count > early_stop_count or longest > early_stop_len:
    if len(top_count_output) > 1:
      top_count_output.sort(reverse = True)

    if len(longest_output) > 1:
      longest_output.sort(reverse = True)

    print("Early stop at Base64")
    return top_count_output[:min(ret_num,len(top_count_output))], \
    longest_output[:min(ret_num,len(longest_output))]

  #test if XOR output is base64
  print("Start XOR output is base64")
  for keylen in range(1, maxlen+1):
    keys = [bytearray(x) for x in xor_base64.smart_xorkeys(string_to_decode, keylen, charset_base64)]
    outputs = [xor_base64.xor(string_to_decode, key) for key in keys]

    for key, output in zip(keys, outputs):
      output = xor_base64.base64_recursive_decode(output)
      eng_count, long_count = check_english.get_eng_counts(output)

      if eng_count > top_count:
        top_count = eng_count

      if long_count > longest:
        longest = long_count

      top_count_output.append((eng_count, key, output))
      longest_output.append((long_count, key, output))

  if top_count > early_stop_count or longest > early_stop_len:
    if len(top_count_output) > 1:
      top_count_output.sort(reverse = True)

    if len(longest_output) > 1:
      longest_output.sort(reverse = True)

    print("Early stop at XOR output base64")
    return top_count_output[:min(ret_num,len(top_count_output))], \
    longest_output[:min(ret_num,len(longest_output))]

  #test guess keylen
  print("Start guess keylen")
  keylen, fitness = guess_xor_length.guess_key_length(string_to_decode)
  #print(keylen, fitness)
  if fitness > 1:
    keys = [bytearray(x) for x in xor_base64.smart_xorkeys(string_to_decode, keylen, charset)]
    outputs = [xor_base64.xor(string_to_decode, key) for key in keys]
    top_count_output = []
    top_count = 0
    for key, output in zip(keys, outputs):
      output = xor_base64.base64_recursive_decode(output)

      eng_count, long_count = check_english.get_eng_counts(output)

      if eng_count > top_count:
        top_count = eng_count

      if long_count > longest:
        longest = long_count

      top_count_output.append((eng_count, key, output))
      longest_output.append((long_count, key, output))

    if top_count > early_stop_count or longest > early_stop_len:
      if len(top_count_output) > 1:
        top_count_output.sort(reverse = True)

      if len(longest_output) > 1:
        longest_output.sort(reverse = True)

      print("Early stop at guess keylen")
      return top_count_output[:min(ret_num,len(top_count_output))], \
      longest_output[:min(ret_num,len(longest_output))]

  #test if XOR output is English
  print("Start XOR output is English")
  for keylen in range(1, maxlen+1):
    keys = [bytearray(x) for x in xor_base64.smart_xorkeys(string_to_decode, keylen, charset)]
    outputs = [xor_base64.xor(string_to_decode, key) for key in keys]

    for key, output in zip(keys, outputs):
      
      eng_count, long_count = check_english.get_eng_counts(output)

      if eng_count > top_count:
        top_count = eng_count

      if long_count > longest:
        longest = long_count

      top_count_output.append((eng_count, key, output))
      longest_output.append((long_count, key, output))

  if top_count > early_stop_count or longest > early_stop_len:
    if len(top_count_output) > 1:
      top_count_output.sort(reverse = True)

    if len(longest_output) > 1:
      longest_output.sort(reverse = True)

    print("Early stop at XOR output English")
    return top_count_output[:min(ret_num,len(top_count_output))], \
    longest_output[:min(ret_num,len(longest_output))]

  #didn't find anything brute force
  print("Start bruteforce")
  for keylen in range(1, 2):
    keys = [bytearray(x) for x in xor_base64.brute_xorkeys(string_to_decode, keylen)]
    outputs = [xor_base64.xor(string_to_decode, key) for key in keys]

    for key, output in zip(keys, outputs):
      
      eng_count, long_count = check_english.get_eng_counts(output)

      if eng_count > top_count:
        top_count = eng_count

      if long_count > longest:
        longest = long_count

      top_count_output.append((eng_count, key, output))
      longest_output.append((long_count, key, output))

  #  if top_count > early_stop_count or longest > early_stop_len:
  if len(top_count_output) > 1:
    top_count_output.sort(reverse = True)

  if len(longest_output) > 1:
    longest_output.sort(reverse = True)

  print("Stop at brute force")
  return longest_output[:min(ret_num,len(longest_output))], \
  top_count_output[:min(ret_num,len(top_count_output))]