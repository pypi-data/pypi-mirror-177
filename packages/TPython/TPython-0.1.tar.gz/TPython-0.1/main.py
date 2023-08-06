import sys
from os import system, name, get_terminal_size
from traceback import format_exc
try:
    from colorama import init as cinit, Fore
except:
    sys.exit('module not found: colorama\npython3 -m pip install colorama')

n = 1
err = False
a = False
namespace = {}

def main():
    global n, err, a
    cinit(autoreset=True)

    def ext(crash=False):
        cl = get_terminal_size().columns
        m = 'Crashed' if crash else 'Process Completed Successfully'
        for i in range((cl-len(m))//2):
            m = f'-{m}-'
        if len(m) != cl:
            m += '-'
        sys.exit(f'{Fore.LIGHTYELLOW_EX}{"-"*cl}\n{m}\n{"-"*cl}' if crash else f'{Fore.LIGHTCYAN_EX}{m}')

    try:
        def exe(inp):
            global err, n
            try:
                exec(inp, namespace)
                err = False
            except Exception:
                print(f'{Fore.LIGHTRED_EX}{format_exc()}')
                err = True
            n += 1

        cl = get_terminal_size().columns
        m = 'Welcome to TPython'
        cl -= 18
        for i in range(cl//2):
            m = f'-{m}-'
        print(f'{Fore.LIGHTCYAN_EX}{m}')

        while True:
            try:
                inp = input(f'{Fore.LIGHTGREEN_EX}[{Fore.LIGHTRED_EX if err else Fore.RESET}{n}{Fore.LIGHTGREEN_EX}]-{Fore.LIGHTCYAN_EX}> {Fore.RESET}')
                if not (inp.isspace() or inp == ''):
                    inp = inp.strip()
                    if inp == 'exit' or inp == 'quit':
                        ext()
                    elif inp == 'clear' or inp == 'cls':
                        system('cls' if name == 'nt' else 'clear')
                        err = False
                    elif inp == 'version':
                        with open('version', 'r') as f:
                            print(f'{Fore.LIGHTCYAN_EX}{f.read()}')
                    else:
                        if inp.endswith(':'):
                            while True:
                                ig = input(f'{Fore.LIGHTGREEN_EX}[{Fore.LIGHTYELLOW_EX}{":"*len(str(n))}{Fore.LIGHTGREEN_EX}]-{Fore.LIGHTYELLOW_EX}> {Fore.RESET}')
                                if ig.strip() == '':
                                    if not a:
                                        a = True
                                    else:
                                        break
                                else:
                                    inp += f'\n\t{ig}'
                            exe(inp)
                            a = False
                        else:
                            exe(inp)
            except KeyboardInterrupt:
                print(f'\n{Fore.LIGHTYELLOW_EX}KeyboardInterrupt')
                err = True
    except Exception:
        print(f'\n{Fore.LIGHTRED_EX}{format_exc()}')
        ext(True)