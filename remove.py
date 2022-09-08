import os

def rmdir(target):
    for root, dirs, files in os.walk(target):
        for file_name in files:
            try:
                os.remove(f'{root}/{file_name}')
                print(f'已刪除 {root}\{file_name}')
            except:
                continue
    for root, dirs, files in os.walk(target):
        for i in dirs:
            try:
                os.rmdir(f'{root}/{i}')
            except:
                continue
    os.rmdir(target)