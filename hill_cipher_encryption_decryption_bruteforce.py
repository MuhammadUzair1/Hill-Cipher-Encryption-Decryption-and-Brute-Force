import numpy as np
import os

# Formating
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Substitution dictionary for mapping letters to numbers
substitution = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
               'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
               'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

# Inverse substitution dictionary for mapping numbers to letters
inverse_substitution = {value: key for key, value in substitution.items()}

def is_modular_inverse_possible(array, modulus_value):
    # Calculate determinant of the array
    determinant = int(np.round(np.linalg.det(array)))
    
    # Calculate the greatest common divisor (GCD) between the determinant and the modulus value
    gcd = np.gcd(determinant % modulus_value, modulus_value)

    # If the GCD is 1, modular inverse exists; otherwise, it doesn't
    return gcd == 1

def encrypt(plain_text, key_matrix):
    # Convert the plain text to uppercase
    plain_text = plain_text.upper()

    # Remove any spaces from the plain text
    plain_text = plain_text.replace(" ", "")

    # Pad the plain text if its length is not a multiple of the key matrix size
    if len(plain_text) % len(key_matrix) != 0:
        padding_length = len(key_matrix) - (len(plain_text) % len(key_matrix))
        plain_text += 'X' * padding_length

    # Initialize the cipher text
    cipher_text = ''

    # Encrypt the plain text
    for i in range(0, len(plain_text), len(key_matrix)):
        # Get the current block of the plain text
        block = plain_text[i:i + len(key_matrix)]

        # Convert the block to a column vector of numbers
        block_vector = np.array([substitution[ch] for ch in block])

        # Multiply the key matrix with the block vector
        encrypted_vector = np.dot(key_matrix, block_vector) % 26

        # Convert the encrypted vector back to a string
        encrypted_block = ''.join([inverse_substitution[num] for num in encrypted_vector])

        # Append the encrypted block to the cipher text
        cipher_text += encrypted_block

    #Checking wheter inverse of key matrix is possible or not
    inverse_possible = is_modular_inverse_possible(key_matrix, 26)
    
    #if possible then:
    if inverse_possible:
        print("\nCipher Decryption Possible with the given key!!\n")
    else:    
        print("\nCipher Decryption Not Possible with the given key!!\n")
        
    return cipher_text

def mod_inverse(a, m):
    """
    Extended Euclidean Algorithm to find modular inverse
    """
    m0 = m
    y, x = 0, 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        m, a = a % m, m
        y, x = x - q * y, y

    if x < 0:
        x += m0

    return x % m0

def decrypt(cipher_text, key_matrix):
    
    #Checking wheter inverse of key matrix is possible or not
    inverse_possible = is_modular_inverse_possible(key_matrix, 26)
    
    #if possible then:
    if inverse_possible:
        # Calculate the determinant of the key matrix
        determinant = int(np.round(np.linalg.det(key_matrix)))

        # Ensure the determinant is non-zero before proceeding
        if determinant % 26 == 0:
            return "Cannot find modular inverse, decryption not possible."

        # Calculate the modular inverse of the determinant
        determinant_inverse = mod_inverse(determinant % 26, 26)

        # Check if the modular inverse exists
        if determinant_inverse == 0:
            return "Modular inverse doesn't exist."

        # Calculate the adjugate matrix
        adjugate_matrix = np.round(determinant_inverse * np.linalg.inv(key_matrix) * determinant) % 26

        # Calculate the inverse key matrix
        inverse_key_matrix = (adjugate_matrix % 26).astype(int)

        # Initialize the decrypted text
        decrypted_text = ''

        # Decrypt the cipher text
        for i in range(0, len(cipher_text), len(key_matrix)):
            block = cipher_text[i:i + len(key_matrix)]
            block_vector = np.array([substitution[ch] for ch in block])

            decrypted_vector = np.dot(inverse_key_matrix, block_vector) % 26
            decrypted_block = ''.join([inverse_substitution[num] for num in decrypted_vector])

            decrypted_text += decrypted_block

        return decrypted_text

    #else 
    else:
        return "Cannot find modular inverse, decryption not possible."
    
def brute_force(plain_text, cipher_text):
    plain_text = plain_text.upper()
    cipher_text = cipher_text.upper()
    for i in range(26):
        for j in range(26):
            for k in range(26):
                for l in range(26):
                    brute_key_matrix = np.array([[i,j],[k,l]])
                    inverse_possible = is_modular_inverse_possible(brute_key_matrix, 26)
                    if inverse_possible:
                        brute_decrypt = decrypt(cipher_text, brute_key_matrix)
                        if brute_decrypt == plain_text.replace(' ', ''):
                            return brute_key_matrix
    return None

def main():
    while True:
        # Clearing the Screen
        os.system('cls')
        print(color.BOLD + '\n\t\t\tWelcome to the Hill Cipher Encryption-Decryption Tool!!\n' + color.END)
        print("Choose an option:")
        print("1. Encryption")
        print("2. Decryption")
        print("3. Brute Force")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1/2/3/4): \n")

        if choice == '1':
            plain_text = input("Enter the plain text: ")
            key_matrix = np.array([[int(input("Enter element [0,0]: ")), int(input("Enter element [0,1]: "))],
                                   [int(input("Enter element [1,0]: ")), int(input("Enter element [1,1]: "))]])
            cipher_text = encrypt(plain_text, key_matrix)
            print("\nCipher Text:", cipher_text)
            option = input("\nChoose an option: 1. Main Menu 2. Exit: ")
            if option == '2':
                break

        elif choice == '2':
            cipher_text = input("Enter the cipher text: ")
            key_matrix = np.array([[int(input("Enter element [0,0]: ")), int(input("Enter element [0,1]: "))],
                                   [int(input("Enter element [1,0]: ")), int(input("Enter element [1,1]: "))]])
            decrypted_text = decrypt(cipher_text, key_matrix)
            print("\nDecrypted Text:", decrypted_text)
            option = input("\nChoose an option: 1. Main Menu 2. Exit: ")
            if option == '2':
                break

        elif choice == '3':
            plain_text = input("Enter the plain text: ")
            cipher_text = input("Enter the cipher text: ")
            key = brute_force(plain_text, cipher_text)
            if key is None:
                print("\nKey not found.")
            else:
                print("\nKey Matrix found after brute force:\n", key)
            option = input("Choose an option: 1. Main Menu 2. Exit: ")
            if option == '2':
                break

        elif choice == '4':
            break

        else:
            print("\nInvalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()