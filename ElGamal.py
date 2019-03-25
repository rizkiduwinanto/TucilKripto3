import base64
import random

def message_to_bytes(input_path):
  with open(input_path, "rb") as file:
    file_byte = file.read()
  return base64.b64encode(file_byte).decode('utf-8')

def encode_char(character):
  return 10 + ord(character.lower())-ord('a')

def decode_code(code):
  return chr(ord('a') + code-10)

def prime_generation():
  pass

def key_generation(random_prime):
  random_int_g = random.randint(0, random_prime-1)
  random_int_x = random.randint(1, random_prime-2)
  h_num = pow(random_int_g, random_int_x) % random_prime
  public_key = (h_num, random_int_g, random_prime)
  private_key = (random_int_x, random_prime)
  return public_key, private_key

def encrypt_char(char, public_key):
  char_int = encode_char(char)
  h_num = public_key[0]
  random_int_g = public_key[1]
  random_prime = public_key[2]
  random_int_k = random.randint(1, random_prime-2)
  a_num = pow(random_int_g, random_int_k) % random_prime
  b_num = (pow(h_num, random_int_k) * char_int) % random_prime
  return a_num, b_num

def decrypt_char(ciphertext, private_key):
  a_num = ciphertext[0]
  b_num = ciphertext[1]
  random_int_x = private_key[0]
  random_prime = private_key[1]
  j_num = pow(a_num, random_prime-1-random_int_x) % random_prime
  char_int = (b_num * j_num) % random_prime
  char = decode_code(char_int)
  return char

if __name__ == "__main__":
  # message = message_to_bytes('Test.txt')
  message = 'Infrastruktur langit utk orang tua menuju akhirat'
  # print(encode_char(message))
  print(message)
  public_key, private_key = key_generation(257)
  encrypted_message = [encrypt_char(m, public_key) for m in message]
  decrypted_message = [decrypt_char(m, private_key) for m in encrypted_message]
  print(''.join(decrypted_message))

    