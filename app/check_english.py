import nltk
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 
import string
import xor_base64
from urllib.request import urlopen

punctuation = set(string.punctuation)

# eng_words_url = 'https://raw.github.com/eneko/data-repository/master/data/words.txt'
# eng_words_read = urlopen(eng_words_url).readlines()

# eng_words = [w.strip().lower().decode("ascii") for w in eng_words_read]

with open("words.txt", "rb") as f:
  eng_words_read = f.readlines()
# # type(eng_words_read[10])
# type(eng_words[10])
eng_words = [w.strip().lower().decode("ascii") for w in eng_words_read]
# type(eng_words[10])

def remove_punc(str):
    return ''.join(c for c in str if c not in punctuation)

def find_percent_english(line):
  total_count = 0
  eng_count = 0
  words = remove_punc(line).lower().split()
  total_count += len(words)
  eng_count += sum(1 for word in words if len(word) > 2 and lemmatizer.lemmatize(word.lower(),'v') in eng_words)
  percentage_eng = 0 if total_count == 0 else (float(eng_count) / total_count * 100)

  return percentage_eng

def find_num_english(line):
  '''
  Find number of English words (separated by spaces)
  '''
  total_count = 0
  eng_count = 0
  words = remove_punc(line).lower().split()
  total_count += len(words)
  eng_count += sum(1 for word in words if len(word) > 2 and lemmatizer.lemmatize(word.lower(),'v') in eng_words)
  #percentage_eng = 0 if total_count == 0 else (float(eng_count) / total_count * 100)
  return total_count, eng_count


def find_num_english_embedded(line):
  '''
  Find number of embedded English words (may not be separated by spaces)
  '''
  eng_count = 0
  words = [word for word in eng_words if word in line.lower()]
  eng_count += sum(1 for word in words if len(word) > 4 and lemmatizer.lemmatize(word.lower(),'v') in eng_words)
  #percentage_eng = 0 if total_count == 0 else (float(eng_count) / total_count * 100)

  return eng_count

def find_longest_english_embedded(line):
  '''
  Find longest embedded English word (may not be separated by spaces)
  '''
  #print(line)
  words = [word for word in eng_words if word in line.lower()]
  if len(words) > 0:
    # print(words)
    return len(max(words, key=len))
  else:
    return 0

def get_eng_counts(output):
  '''
  return english word count and length of longest word
  '''
  # output = xor_base64.base64_recursive_decode(output)

  eng_count = 0
  long_count = 0

  try:
    long_count = find_longest_english_embedded(output.decode("ascii"))
    _, eng_count = find_num_english(output.decode("ascii"))
  except:
    try:
      long_count = find_longest_english_embedded(str(output))
      _, eng_count = find_num_english(str(output))
    except:
      pass

  return eng_count, long_count