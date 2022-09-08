from pytube import YouTube, Playlist
from flask import send_from_directory
import platform, zipfile, os

def download_playlist(url, url_root='', type=None, email=''):
    list = Playlist(url)
    title = list.title
    des = 'download/'+title
    for i in list.videos:
        i.streams.get_highest_resolution().download(des)
    with zipfile.ZipFile(f'{des}.zip', 'w') as zf:
        for root, dirs, files in os.walk(des):
            for file_name in files:
                path = f'{root}/{file_name}'
                zf.write(path)
    return send_from_directory('download', f'{title}.zip', as_attachment = True)

def download_one(url, res, url_root='', type=None, email=''):
    video = YouTube(url)
    if res == '':
        file_path = video.streams.get_highest_resolution().download('download')
    else:
        file_path = video.streams.filter(res=res, progressive=True)[0].download('download')
    if platform.system() != 'Windows':
        file_name = file_path.split('/')[-1]
    else:
        file_name = file_path.split('\\')[-1]
    return send_from_directory('download', file_name, as_attachment=True)
    # if type == None:
    #     return send_from_directory('download', file_name, as_attachment=True)
    # else:
    #     send_email(email, file_name, url_root)

def size(video:dict):
    size = 0
    if video['type'] == 'video':
        v = YouTube(video['source'])
        size = v.streams.get_highest_resolution().filesize
    else:
        v = Playlist(video['source'])
        for i in v.videos:
            size += i.streams.get_highest_resolution().filesize
    size_mb = round(size/1024/1024)
    return size_mb

def download_from_email(file_name):
    return send_from_directory('download', file_name, as_attachment=True)