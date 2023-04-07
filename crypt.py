import os
from Crypto.Cipher import AES

#Encryption for storage of tokens

def get_user_input():
    key = input("Please enter the encryption key: ")
    key = bytes(key, 'utf-8')
    filename = input("Please enter the filename: ")
    return key, filename

def encrypt_file(key, filename):
    chunk_size = 64 * 1024
    output_filename = filename + '.encrypted'
    file_size = str(os.path.getsize(filename)).zfill(16)
    iv = os.urandom(16)

    encryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(filename, 'rb') as infile:
        with open(output_filename, 'wb') as outfile:
            outfile.write(file_size.encode('utf-8'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunk_size)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

    print(f"Encrypted file {filename} as {output_filename}")

def decrypt_file(key, filename):
    chunk_size = 64 * 1024
    output_filename = filename[:-10]
    
    with open(filename, 'rb') as infile:
        file_size = int(infile.read(16))
        iv = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(file_size)

    print(f"Decrypted file {filename} as {output_filename}")

key, filename = get_user_input()
#encrypt_file(key, filename)
decrypt_file(key, filename)
