from PIL import Image
from cryptography.fernet import Fernet
import math
import os
import re
import binascii
import itertools
import base64



def encryption():
    word = input("Give message to encrypt: ")
    #key = input("\nGive key to encrypt with: \n")

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(bytes(word, encoding='utf-8'))

    print("Key: " + str(key) + "\n")
    print(cipher_text)


def decryption():
    word = input("Give message to decrypt: \n")
    key = input("\nGive key to decrypt with: \n")

    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(bytes(word, encoding='utf-8'))

    print("\n"+str(plain_text.decode("utf-8")))


def brute_force(messages, method):
    message_perm = ""
    text = ""

    # Decryption key
    if method == "fernet":
        cipher_suite = Fernet( input("\nGive key to decrypt with: "))

    # Searching all the possible combinations
    for permutation in itertools.permutations(messages):
        #print (combination)
        for perm in permutation:
            message_perm += perm
        try:
            if method == "base64":
                plain_text = (base64.b64decode(message_perm)).decode("utf-8")
                print("\nThe hidden message is:\n"+plain_text)
                message_perm = ""
                #break
            if method == "fernet":
                plain_text = cipher_suite.decrypt(bytes(message_perm, encoding='utf-8'))
                print("\nThe hidden message is:\n"+str(plain_text.decode("utf-8")))
                break
        except:
            message_perm = ""
            pass


def extract():
    path = "./crack_images/"
    images = []
    messages = []

    # Get all images from the specific directory
    for r, d, i in os.walk(path):
        for image in i:
            if '.png' in image:
                images.append(os.path.join(r, image))
   
    # Check all images in the specific directory 
    for i in images:
        # Input message to crack
        img = Image.open(i, 'r')
        pix = img.load()

        # Pattern to search
        pattern = re.compile("[-A-Za-z0-9+=_]{14,}")
        message = ""

        # Iterate through all the pixels of the image
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                r, g, b = pix[x, y]

                # Convert rgb's LSB to binary and print it
                if r % 2 == 1:
                    r = 1
                else:
                    r = 0

                if g % 2 == 1:
                    g = 1
                else:
                    g = 0

                if b % 2 == 1:
                    b = 1
                else:
                    b = 0

                message += str(r) + str(g) + str(b)

        # Convert the binary to ascii
        message = (int(message, 2).to_bytes((len(message) + 7) // 8, 'big')).decode("latin-1")

        # Match the pattern inside the ascii text
        matches = re.findall(pattern, str(message))
        print("\nPossible messages:")
        for m in matches:
            messages.append(m)
            print(m)

"""
    print("\nSelect method: ")
    while True:
        print("1. Base64")
        print("2. Fernet")

        choice = input("")
        print("")

        if choice == "1":
            method = "base64"
            break
        elif choice == "2":
            method = "fernet"
            break
        else:
            print("Please make a choice: ")

    brute_force(messages, method)
"""


def hide():
    # Input message and converse it to binary
    word = input("Give message to hide: ")
    bin_word = (''.join(format(ord(x), '08b') for x in word))

    # Input original image name
    img = Image.open("./original_images/" + input("Give the name of the original image: "), 'r')
    pix = img.load()

    # Input the name of the encoded image to export
    img_output = input("Give the name of the output image: ")

    # Counters for r g b values
    bit1 = 0
    bit2 = 1
    bit3 = 2

    # Iterate through the pixels
    for x in range(400, 401):
        for y in range(math.ceil(len(bin_word) / 3)):
            try:
                r, g, b = pix[x, y]

                # Change the the rgb value to odd and even based on the binary value
                if bin_word[bit1] == "1":
                    if r % 2 == 0:
                        r += 1
                else:
                    if r % 2 == 1:
                        r -= 1

                if bin_word[bit2] == "1":
                    if g % 2 == 0:
                        g += 1
                else:
                    if g % 2 == 1:
                        g -= 1

                if bin_word[bit3] == "1":
                    if b % 2 == 0:
                        b += 1
                else:
                    if b % 2 == 1:
                        b -= 1

                pix[x, y] = (r, g, b)

                bit1 = bit1 + 3
                bit2 = bit2 + 3
                bit3 = bit3 + 3
            except IndexError:
                pix[x, y] = (r, g, b)
                break

    # Save the new image
    img.save("./encoded_images/" + img_output)


def analyze():
    # Input message and converse it to binary
    img = Image.open("./original_images/" + input("Give image name: "), 'r')
    pix = img.load()

    message = ""

    # Print all the pixels of the image
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = pix[x, y]
            
            # Example
            #if r != 0 or g != 0 or b != 0:
                #print(r, g, b)
            
            # Convert rgb to binary and print it
            if r % 2 == 1:
                r = 1
            else:
                r = 0

            if g % 2 == 1:
                g = 1
            else:
                g = 0

            if b % 2 == 1:
                b = 1
            else:
                b = 0

            message += str(r) + str(g) + str(b)

    # Write the binary into a file
    with open("results.txt", 'w') as fp:
        fp.write(message + '\n')


def main():
    choice = '0'

    # Menu
    while choice == '0':
        print("1. Analyze")
        print("2. Hide")
        print("3. Extract")
        print("4. Encrypt")
        print("5. Decrypt")

        choice = input("")
        print("")

        if choice == "1":
            analyze()
        elif choice == "2":
            hide()
        elif choice == "3":
            extract()
        elif choice == "4":
            encryption()
        elif choice == "5":
            decryption()
        else:
            print("Please make a choice: ")
    print("\nFinished!")


# Calling main function
main()
