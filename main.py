from ElGamal import * 
import click
import os

@click.command()
@click.option('--file', type=click.Path(), help='File apa saja untuk di dekripsi/enkripsi. Jika tidak ada, akan ada prompt')
@click.option('--private_key', type=click.Path(), help='Private Key')
@click.option('--decrypt/--encrypt', '-d/-e', help='Menentukan enkripsi/dekripsi')
def program(file, decrypt, private_key):
  if decrypt:
    if file:
      message = read_enc_message(file)
      if private_key:
        private_key = read_private_key(private_key)
      else:
        y = click.prompt('Enter num ')
        p = click.prompt('Enter prime')
        private_key = (y, p)
      filename = os.path.splitext(file)[0]
      decrypted_message = decrypt_message(message, private_key)
      str_decrypted = ''.join(decrypted_message)
      write_message(str_decrypted, filename)
    else:
      click.echo('No Ciphertext!!')
  else:
    if file:
      filename = os.path.splitext(file)[0]
      message = message_to_bytes(file)
    else:
      text = click.prompt('Enter a text ')
      filename = click.prompt('Enter filename ')
      message = text
    prime = prime_generation(1000, 1100)
    public_key, private_key = key_generation(prime)
    write_private_key(private_key, filename)
    write_public_key(public_key, filename)
    enc_message = encrypt_message(message, public_key)
    write_enc_message(enc_message, filename)

if __name__ == "__main__":
  program()