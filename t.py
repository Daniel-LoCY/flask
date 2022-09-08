from pytube import YouTube
import re

# def get_res(url=''):
#     video = YouTube('https://www.youtube.com/watch?v=in8NNzwFa-s')
#     regex = re.compile('.*abr="(\d*)kbps".*')

#     res_list = []

#     for i in video.streams.filter(type='audio'):
#         try:
#             result = regex.findall(str(i))
#             if len(result) != 0: 
#                 res_list.append(int(result[0]))
#         except:
#             continue
#     print(res_list)
#     res_list = sorted(list(set(res_list)))
#     for index, i in enumerate(res_list):
#         res_list[index] = str(i) + 'kbps'

#     return { 'res' : res_list }

# print(get_res()['res'])

video = YouTube('https://www.youtube.com/watch?v=in8NNzwFa-s')
video.streams.get_by_itag(251).download('download')
video.streams.get_by_itag(135).download('download')

from moviepy.editor import *

a = VideoFileClip('download/蘇打綠 sodagreen -【小情歌】Official Music Video.mp4')

if a.audio == None:
    b = AudioFileClip('download/蘇打綠 sodagreen -【小情歌】Official Music Video.webm')
    a = a.set_audio(b)
    a.write_videofile('download/merge.mp4')