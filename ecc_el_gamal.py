from libs.utils import *
from libs.ecc import Point, ECC
import math
import random
import argparse


def encode(k, n, p, a, b, message_byte):
    """Return encoded point"""
#     m = encode_char(message_char)
    m = encode_byte(message_byte)
    # Find solveable y
    for i in range(1, k):
        x = generate_x(m, k, i)
        y = is_y_exist(p, a, b, x)
        if (y != -1):
            break
    return Point(x, y)

def decode(k, x):
    """Return message char"""
    code = math.floor((x-1)/k)
#     return decode_code(code)
    return decode_int(code)

@timer
def do_encoding(k, n, p, a, b, messages):
    """Do the encoding things"""
    enc_messages = [encode(k, n, p, a, b, m) for m in messages]
    return enc_messages


@timer
def do_decoding(k, message_point):
    """Do the decoding things"""
    dec_messages = [decode(k, point.x) for point in message_point]
    return dec_messages

def generate_public_key(file_name, ecc, basis_point, private_key):
  pub = ecc.iteration(basis_point, private_key)
  to_write = "{},{}".format(pub.x, pub.y)
  with open("keys/{}".format(file_name),"w") as f:
    f.write(to_write)
    f.close()
    print("created ",file_name)

def generate_private_key(file_name, n):
  pri = random.randint(1,n)
  with open("keys/{}".format(file_name), "w") as f:
    f.write(str(pri))
    f.close()
    print("created ",file_name)
  return pri

def generate_keys(ecc, basis_point, n):
  for f_name in ["sender","receiver"]:
    pri = generate_private_key("{}.pri".format(f_name), n)
    generate_public_key("{}.pub".format(f_name),ecc, basis_point, pri)

def read_public_key(file_path):
  with open(file_path,"r") as f:
    pub = f.read()
    f.close()
    pub = pub.split(",")
    return Point(int(pub[0]),int(pub[1]))

def read_private_key(file_path):
  with open(file_path,"r") as f:
    pri = f.read()
    f.close()
    return int(pri)


def main(args):
  # CONFIG
  k = 10
  p = 2570
  a = -1
  b = 188
  n = 727
  str_message = bytes("hariinihujan","utf-8")

  # ECC Elgamal
  print("[ Initializing ECC El Gamal ]")
  ecc = ECC(a, b, p)
  x = -1
  y = -1
  while (y == -1):
    x += 1
    y = is_y_exist(p,a,b,x)
  point_basis =  Point(x,y) if (y != -1) else Point.INFINITY
  print("Basis:",point_basis,"is_on_curve:",ecc.is_on_curve(point_basis))

  ####
  print("ECC El Gamal")
  print("(1) Generate keys")
  print("(2) Simulate sending receiving")
  print("Choice: ",end="")
  choice = int(input())

  if (choice == 1):
    generate_keys(ecc, point_basis, n)
    exit()
  else:
    # Checking arguments
    sender_private_path = args.sender_pri
    sender_pub_path = args.sender_pub
    receiver_private_path = args.receiver_pri
    receiver_pub_path = args.receiver_pub
    with open(args.file_path, "rb") as f:
      messages = f.read()
      f.close()

  # Alice's
  print("\n[ Alice's ]")
  private_a = read_private_key(sender_private_path)
  public_a = read_public_key(sender_pub_path)
  print("type public a")
  print(type(public_a))
  print("Alice's public point:",public_a,"is_on_curve:",ecc.is_on_curve(public_a))

  # Bob's
  print("\n[ Bob's ]")
  private_b = read_private_key(receiver_private_path)
  public_b = read_public_key(receiver_pub_path)
  print("Bob's public point:",public_b,"is_on_curve:",ecc.is_on_curve(public_b))

  # Encrypting messages 
  print("\n[ Encrypting ]")
  print("Original message:",messages)
  encoded_messages = do_encoding(k, n, p, a, b, messages)
  print("Encoded message: ",encoded_messages)
  choosen_k = k
  encrypted_messages = [
      (ecc.iteration(point_basis, choosen_k),
      ecc.add(point_message, ecc.iteration(public_b, choosen_k)))
      for point_message in encoded_messages
  ]
  print("Encrypted message: ", encrypted_messages)


  # Decrypting messages 
  print("\n[ Decrypting ]")
  decrypted_messages = [
      ecc.subtract(
          message[1],
          ecc.iteration(message[0], private_b)
      )
      for message in encrypted_messages
  ]
  print("Decrypted point messages: ",decrypted_messages)
  decoded_messages = (do_decoding(choosen_k, decrypted_messages))
  print("Decoded messges: ",decoded_messages)
  message = b"".join(decoded_messages)
  print("Message: ",message)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file_path")
  parser.add_argument("sender_pub")
  parser.add_argument("sender_pri")
  parser.add_argument("receiver_pub")
  parser.add_argument("receiver_pri")
  main(parser.parse_args())