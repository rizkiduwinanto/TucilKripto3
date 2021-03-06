import base64
import random
import time
import functools
import os

def timer(func):
    """Record elapsed time in a function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        t = time.time()
        func(*args, **kwargs)
        print("[%s] Elapsed %.6f second" % (func.__name__, time.time()-t))
        return func(*args, **kwargs)
    return wrapper_timer

def message_to_bytes(input_path):
  print("File size of plaintext : {} bytes".format(os.path.getsize(input_path)))
  filename, extension = input_path.split('.')
  with open(input_path, "rb") as file:
    file_byte = file.read()
  bytes = base64.b64encode(file_byte).decode('utf-8')
  return bytes + '#' + extension

def write_message(message, output_path):
  byte, extension = message.split('#')
  file_byte = base64.b64decode(byte.encode('utf-8'))
  output_path = output_path + '.' + extension
  with open(output_path, 'wb') as file:
    file.write(file_byte)
  print("File size of decrypted plaintext : {} bytes".format(os.path.getsize(output_path)))

def write_public_key(public_key, output_path):
  h_num, random_int_g, random_prime = public_key
  with open(output_path + '.pub', 'w') as file:
    file.write(str(h_num) + '#' + str(random_int_g) + '#' + str(random_prime))
  
def read_public_key(input_path):
  with open(input_path, 'r') as file:
    str = file.read()
  public_key = list(map(int, str.split('#')))
  return tuple(public_key)

def write_private_key(private_key, output_path):
  random_int_x, random_prime = private_key
  with open(output_path + '.pri', 'w') as file:
    file.write(str(random_int_x) + '#' + str(random_prime))
  
def read_private_key(input_path):
  with open(input_path, 'r') as file:
    str = file.read()
  private_key = list(map(int, str.split('#')))
  return tuple(private_key)

def read_enc_message(input_path):
  with open(input_path, "r") as file:
    string = file.read()
  enc_message = list(tuple(map(int, m.split('#'))) for m in string[:-1].split('\n'))
  return enc_message

def write_enc_message(message, output_path):
  string = ''.join((str(a) + '#' + str(b) + '\n') for _, (a, b) in enumerate(message))
  with open(output_path + '_encrypted.txt', 'w') as file:
    file.write(string)
  print("File size of ciphertext : {} bytes".format(os.path.getsize(output_path + '_encrypted.txt')))

def encode_char(character):
  return ord(character)

def decode_code(code):
  return chr(code)

def prime_generation(min, max):
  """Generasi bilangan prime acak"""
  return random.choice([x for x in range(min, max) if not [t for t in range(2, x) if not x % t]])

def key_generation(random_prime):
  """Generasi kunci publik dan privat untuk enkripsi"""
  random_int_g = random.randint(0, random_prime-1)
  random_int_x = random.randint(1, random_prime-2)
  h_num = pow(random_int_g, random_int_x) % random_prime
  public_key = (h_num, random_int_g, random_prime)
  private_key = (random_int_x, random_prime)
  return public_key, private_key

def encrypt_char(char, public_key):
  """Enkripsi char dari message"""
  char_int = encode_char(char)
  h_num, random_int_g, random_prime = public_key
  random_int_k = random.randint(1, random_prime-2)
  a_num = pow(random_int_g, random_int_k) % random_prime
  b_num = (pow(h_num, random_int_k) * char_int) % random_prime
  return a_num, b_num

@timer
def encrypt_message(message, public_key):
  """Enkripsi char dari message"""
  return [encrypt_char(m, public_key) for m in message]

def decrypt_char(ciphertext, private_key):
  """Deskripsi char dari message"""
  a_num, b_num = ciphertext
  random_int_x, random_prime = private_key
  j_num = pow(a_num, random_prime-1-random_int_x) % random_prime
  char_int = (b_num * j_num) % random_prime
  char = decode_code(char_int)
  return char

@timer
def decrypt_message(message, private_key):
  """Deskripsi message"""
  return [decrypt_char(m, private_key) for m in message]

if __name__ == "__main__":
  file = 'data/rinaldi.jpg'
  filename, extension = file.split('.')
  message = message_to_bytes(file)
  print(message)
  prime = prime_generation(100, 1000)
  print(prime)
  public_key, private_key = key_generation(prime)
  write_private_key(private_key, filename)
  write_public_key(public_key, filename)
  encrypted_message = encrypt_message(message, public_key)
  write_enc_message(encrypted_message, filename)

  private_key = read_private_key('data/rinaldi.pri')
  encrypted_message = read_enc_message('data/rinaldi_encrypted.txt')
  decrypted_message = decrypt_message(encrypted_message, private_key)
  str_decrypted = ''.join(decrypted_message)
  write_message(str_decrypted, 'data/rinaldi_decrypted')
    