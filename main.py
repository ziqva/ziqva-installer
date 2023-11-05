import app_menu
import scanner
import readchar
import chalk
import time
import installer

red = chalk.Chalk('red')
green = chalk.Chalk('green')

if __name__ == "__main__":
    while True:
        try :
            app: object = app_menu.get_app()
            app_menu.clear_console()
            data: list or None = scanner.scan(app)
            appname: str = app['name']
            if data == None :
                raise Exception(f'Binnary source for app "{appname}" is not exists')
            app_menu.clear_console()
            msg: str = f'''
Latest version of app "{appname}" found!
------------ DETAIL ------------
File    : {data['filename']}
Size    : {data['size_mb']}mb
Version : {data['version']}
--------------------------------

Do you want to install this version (Y/N) default: Y ?'''
            install_confirm: str = input(green(msg, bold=True))
            if(str.lower(install_confirm) == 'n') :
                app_menu.clear_console()
                print(red('Operation canceled by user!', bold=True))
                time.sleep(3)
            else :
                app_menu.clear_console()
                zip_path: str = installer.download(download_url=data['download'], title=f'{data["filename"]} - {data["version"]}')
                main_executable_path: str or None = installer.install(zip_path, appname, data['version'])
                installer.create_desktop_shortcut(main_executable_path, appname)
                print(green(f'App "{appname}" is already on desktop !'))
                print(green('\nPress any key to continue...'))
                input()
        except Exception as err :
            print(red(f'Error: ' + str(err), bold=True))
            print('\n\nPress any key to continue...')
            key = readchar.readkey()

