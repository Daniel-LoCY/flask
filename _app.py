import os
from flask import Flask, render_template, send_from_directory, request, redirect
from pytube import YouTube, Playlist
from flask_cors import cross_origin, CORS
import zipfile

app = Flask(__name__)

@app.route('/watch', methods=['GET'])
def ts():
    try:
        arg = request.args['v']
        com = 'pytube https://www.youtube.com/watch?v=' + arg
        os.system(com)
        url = 'https://www.youtube.com/watch?v=' + arg
        video = YouTube(url)
    # * ? > < ; & ! [ ] | \ ' " ` ( ) { }
    #s = ['*', '?', '>', '<', ';', '&', '!', '[', ']', '|', "'", ]
        title = video.title.replace("'", "")
        title = title.replace('.', '')
        title = title.replace('/', '')
        title = title.replace('\\', '')
        title = title.replace('#', '')
        title = title.replace(':', '')
        result = title + '.mp4'
        dst = 'download/' + result
        os.rename(result, dst)
        if os.path.exists(result):
            os.remove(result)
        return send_from_directory('download', result, as_attachment=True)
    except: 
        return "<h1>下載失敗 很抱歉</h1"
    
@app.route('/playlist', methods = ['GET'])#https://www.youtube.com/playlist?list=PL3Cef_lHMDU5STm_ae4iZCvhtMPj43Bbt
def playList():
        arg = request.args['list']
        url = 'https://www.youtube.com/playlist?list=' + arg
        list = Playlist(url)
        os.system('rm -rf video.zip')
        if os.path.exists(list.title):
            os.system('rm -rf ' + list.title)
        os.system('pytube ' + url)
        with zipfile.ZipFile(f'video.zip', 'w') as zf:
            for root, dirs, files in os.walk(list.title):
                for file_name in files:
                    zf.write(f'{root}/{file_name}')
        os.system('mv ' + list.title + '/* download/')
        os.system('rm -rf ' + list.title)
        return send_from_directory('./', 'video.zip', as_attachment = True)
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/upload', methods=['POST'])
def upload():
    c=''
    title = request.form.get('title')
    content = request.form.get('content')
    if "\n" in content:
        content = content.replace('\n', '<br/>')
    r = request.values['title']
    if title != '' and content != '':
        with open('static/chat.txt', 'r') as f:
            r = f.read()
            n = r.rfind('}')
            result = eval(r)
            index = (len(result))
            try:
                id = result[index-1]['id']
            except:
                id = 1
            if n == -1:
                n = r.rfind('[')
                c = r[:n+1] + f'\n    {{"id":{id}, "title":"{title}", "content":"{content}"}}' + r[n+1:]
            else:
                c = r[:n+1] + f'\n    ,{{"id":{id+1}, "title":"{title}", "content":"{content}"}}' + r[n+1:]
        print(c)
        with open('static/chat.txt', 'w') as w:
            w.write(c)
    return (c)

@app.route('/delete', methods=['POST'])
def delete_chat():
    answer = request.form.get('answer')
    if answer == '5627abcd':
        id = request.form.get('id')
        with open('static/chat.txt','r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if f'"id":{id}' in lines[i]:
                    lines.remove(lines[i])
                    if ',{' in lines[i] and i == 1:
                        lines[i] = lines[i].replace(',{', '{')
                    with open('static/chat.txt', 'w') as f:
                        f.writelines(lines)
                        break
    return "1"

@app.route('/download', methods=['GET'])
def download():
    return render_template('download.html')

@app.route('/file', methods=['GET'])
def file():
    path = 'jupyter-notebook-dir/For-File'
    file_list = []
    files = os.walk(path)
    for dirpath, dirname, filenames in files:
        for filename in filenames:
            file_list.append({ 'name' : filename })
    ret = {
        'file_name' : file_list
    }
    return ret

@app.route('/download_file', methods=['GET'])
def download_file():
    filename = request.args['filename']
    print(filename)
    dirname = 'jupyter-notebook-dir/For-File/'
    print(dirname)
    return send_from_directory(dirname, filename, as_attachment=True)

"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('server.crt', 'server.key'))
    """
