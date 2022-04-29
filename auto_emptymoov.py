from glob import glob
import os
import re
import subprocess
from pathlib import Path
from time import sleep

mydrive = '哔哩哔哩'
room = "集智俱乐部"
concat_room = "_swarma"
gd ="./virltu"
os.system(f"mkdir -p {gd}/{mydrive}/{concat_room}")

all_title = []
allFpath = sorted(glob(f'{gd}/{mydrive}/{room}/*flv'), reverse=False)

for i in allFpath:
    title = re.findall(r'\[(.+?) .+?\]\[.+?\]\[(.+?)\]', i)[0]
    if title not in all_title:
        all_title.append(title)
for i in all_title:
    print(i)



## 检查分辨率
def check_res(all_path):
    all_res = dict()
    for i in allFpath:
        
        output = subprocess.getoutput(
            f'ffprobe -v fatal -hide_banner -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{i}"')
        # output = output.split('\n')[1]
        output = output.replace(',','x')
        if not all_res.get(output):
            all_res[output] = [i]
        else:
            all_res[output].append(i)

    if len(all_res) > 1:
        print(">1 res:", all_res.keys())
    return all_res
    
def ts_concat(all_path, output_filepath, res):

    if Path(output_filepath).is_file():
        return 'skip'

    s_ts = "concat:"
    for i in all_path[:]:
        filename_nopath = i.split('/')[-1]
        cmd = f'ffmpeg -fflags +discardcorrupt -i "{i}" -c copy -bsf:v h264_mp4toannexb -f mpegts -y "/tmp/{filename_nopath}.ts"'
        # print(cmd)
        os.system(cmd)
        # f'''ffmpeg -hide_banner -loglevel warning -ss 00:00:00.3 -to {new_dur} -accurate_seek -i "{i}" -codec copy -avoid_negative_ts 1 -y "{i}.{fix}" ''')
        s_ts += f'/tmp/{filename_nopath}.ts|'

    # print()

    cmd = f'ffmpeg -analyzeduration 2147483647 -probesize 2147483647 -i "{s_ts[:-1]}" -c copy -bsf:a aac_adtstoasc -movflags frag_keyframe+empty_moov -y "{output_filepath}"'
    cmd_log = f''' 2> "{gd}/{mydrive}/{concat_room}/_{title}_{room}_{date.replace('-','')}_{res}_ts.log"'''
    cmd = cmd + cmd_log
    # print(cmd)
    os.system(cmd)
    return 'end'

for date, title in all_title:
    if '中国空间站首次太空授课' in title: continue
    allFpath = sorted(glob(f'{gd}/{mydrive}/{room}/*{date}*{title}*flv'),  reverse= False)
    all_res = check_res(allFpath)
    for res, file_list in all_res.items():
        output_filepath = f"{gd}/{mydrive}/{concat_room}/{title}_{room}_{date.replace('-','')}_{res}_ts.mp4"
        print(title, date, res, 'begin ...', end=' ')
        concat_result = ts_concat(file_list, output_filepath, res)
        print(concat_result)
    for i in sorted(glob(f'/tmp/*.ts')):
        os.system(f'''rm -f "{i}"''')
    sleep(10)
