import os
import sys
import json
import plyer


def setup():
    if not os.path.exists(f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade'):
        os.mkdir(f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade')

    if not os.path.exists(f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json'):
        with open(file=f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json', mode='w', encoding='utf-8') as file:
            file.write('{}')
    
    with open(file=f'{os.path.expanduser("~")}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Shade.bat', mode='w', encoding='utf-8') as file:
        file.write(f'@echo off\nstart /low {sys.argv[0]}\nexit')

    with open(file=f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json', mode='r', encoding='utf-8') as file:
        data=dict(json.load(fp=file))

        data.setdefault('token', 'ENTER YOUR TOKEN')
        data.setdefault('prefix', '.')
        data.setdefault('activity', {}).setdefault('application id', 1042447620058128484)
        data.setdefault('activity', {}).setdefault('asset id', 1042449330117808229)

        with open(file=f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json', mode='w', encoding='utf-8') as file:
            json.dump(obj=data, fp=file, indent=2)

    with open(file=f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json', mode='r', encoding='utf-8') as file:
        data=dict(json.load(fp=file))

        if data.setdefault('token', 'ENTER YOUR TOKEN') == 'ENTER YOUR TOKEN':
            os.startfile(f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json')
            plyer.notification.notify(title='Установка', message='Вставьте токен своего аккаунта\n( "token": "Сюда" )', timeout=20)

def start():
    from client import client
    if os.path.exists(f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade'):
        with open(file=f'{os.path.expanduser(path="~")}\AppData\Roaming\.Shade\config.json', mode='r', encoding='utf-8') as file:
            data=dict(json.load(fp=file))
            if data.setdefault('token', 'ENTER YOUR TOKEN') != 'ENTER YOUR TOKEN':
                try:
                    client.run(data.setdefault('token', ''), bot=False)
                except:
                    plyer.notification.notify(title='Ошибка', message='Проверьте подключение к интернету или валидность токена', timeout=20)


if __name__ == '__main__':
    setup()
    start()
