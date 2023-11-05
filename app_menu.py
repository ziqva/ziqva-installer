import chalk
import os
import readchar

apps: list = [
    {"name": "Tiktok Uploader", "prefix": "Tiktok Uploader"},
    {"name": "AsistenQ Owner", "prefix": "AsistenQ Owner"},
    {"name": "AsistenQ Admin", "prefix": "AsistenQ Admin"},
    {"name": "AsistenQ Chat", "prefix": "AsistenQ Chat"},
    {"name": "Tokped Uploader", "prefix": "Tokped Uploader"}
]

green = chalk.Chalk('green')

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_app() -> object:
    selected: int = 0
    while (True):
        clear_console()
        print(green('Pilih aplikasi:'))
        for i in range(len(apps)):
            app: object = apps[i]
            prefix: str = '     >' if selected == i else '     -'
            text: str = green(f'{prefix} {app["name"]}', bold=selected == i)
            print(text)
        key_pressing: any = readchar.readkey()
        if key_pressing == readchar.key.UP and selected > 0:
            selected -= 1
        elif key_pressing == readchar.key.DOWN and selected < (len(apps) - 1):
            selected += 1
        elif key_pressing == readchar.key.ENTER or key_pressing == readchar.key.ENTER_2 :
            return apps[selected]
