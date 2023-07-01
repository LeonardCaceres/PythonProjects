import pyfiglet
pyfiglet.print_figlet('file encoder', font = 'slant')
import pyAesCrypt
from pathlib import Path

if __name__ == '__main__':
    print('     Hello!')
    try:
        print('What do you want?\n• encrypt file(1)        • decrypt file(2)\n• exit(3)\n')
        choice = int(input('Enter the numbers in parentheses: '))
        if choice == 3:
            x = 1 / 0
        file_path_enter = input('\nEnter the path to the file: ')
        file = Path(file_path_enter)
        password = input('\nEnter the (en/de)cryption password: ')
        pyfiglet.print_figlet('... in progress ...')
        if choice == 1:
            pyAesCrypt.encryptFile(f'{file}', f'{file}.aes', password)
        elif choice == 2:
            pyAesCrypt.decryptFile(f'{file}.aes', f'{file}', password)
        pyfiglet.print_figlet('completed')
    except ZeroDivisionError:
        print('exit(3)')
    except:
        print('\n\n\n\nSomething went wrong...\nMake sure everything is correct\n------------exit---------------')