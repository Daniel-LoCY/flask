from pytube import YouTube
import re

def get_res(url):
    video = YouTube(url)
    regex = re.compile('.*mime_type="video/mp4".*res="(\d*)p".*')

    res_list = []

    try:

        for i in video.streams.filter(type='video', progressive=True):
            try:
                result = regex.findall(str(i))
                if len(result) != 0: 
                    res_list.append(int(result[0]))
            except:
                continue
        
        res_list = sorted(list(set(res_list)))
        for index, i in enumerate(res_list):
            res_list[index] = str(i) + 'p'

        return { 'res' : res_list }
    except:
        return { 'res' : 'error' }

    # ok = []
    # res = []
    # video_info = {}
    # fil = video.streams.filter(type='video', mime_type='video/mp4')
    # for i in fil:
    #     a = re.findall(r'itag="(\d+)".*res="(\d+)p".*vcodec="avc1..*progressive="False"', str(i))
    #     b = re.findall(r'itag="(\d+)".*res="(\d+)p".*vcodec="avc1..*progressive="True"', str(i))
    #     if len(a) == 1:
    #         if a[0][1] not in video_info.keys():
    #             res.append(int(a[0][1]))
    #             video_info[a[0][1]] = {'itag':int(a[0][0]), 'pro':'false'}
    #     if len(b) == 1:
    #         res.append(int(b[0][1]))
    #         video_info[b[0][1]] = {'itag':int(b[0][0]), 'pro':'true'}
    # ok = sorted(list(set(res)))
    # for i in range(len(ok)):
    #     if video_info[str(ok[i])]['pro'] == 'false':
    #         ok[i] = f'{str(ok[i])}p  (需轉檔)'
    #     else:
    #         ok[i] = f'{str(ok[i])}p'
    
    # return { 'res' : ok }