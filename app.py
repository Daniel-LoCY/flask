import os
from flask import Flask, render_template, send_from_directory, request, redirect
from pytube import YouTube, Playlist
from flask_cors import CORS
import zipfile
from remove import rmdir
from download_video import download_playlist, download_one, size, download_from_email
from line_notify import sent

app = Flask(__name__)
cors = CORS(app, resources = { r'*' : { 'origins' : '*' } })

@app.route('/watch', methods=['GET'])
def watch():
    try:
        arg = request.args['v']
        res = ''
        try:
            res = request.args['res']
        except:
            pass
        url = 'https://www.youtube.com/watch?v=' + arg
        return download_one(url, res)
    except Exception as e:
        print(e) 
        return "<h1>下載失敗 很抱歉</h1>"
    
@app.route('/playlist', methods = ['GET'])
def playList():
    try:
        arg = request.args['list']
        url = 'https://www.youtube.com/playlist?list=' + arg
        return download_playlist(url)
    except Exception as e:
        print(e)
        return "<h1>下載失敗 很抱歉</h1>"

@app.route('/res')
def get():
    from find_res import get_res
    url = request.args['url']
    return get_res(url)

@app.route('/size')
def get_size():
    from download_video import size
    return ''
    
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
    # print(filename)
    dirname = 'jupyter-notebook-dir/For-File/'
    # print(dirname)
    return send_from_directory(dirname, filename, as_attachment=True)

@app.route('/webhook', methods=['POST'])
def webhook():
    repos = request.form.get('repository')
    return str(repos)

@app.route('/test')
def test():
    return 'test OK'

if __name__ == '__main__':
    app.run()
