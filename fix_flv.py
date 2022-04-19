import subprocess,re
from glob import glob

def time_convert_ffmpeg(time):
    time = time.split(":")
    if len(time) == 3:
        time = int(time[0]) * 3600 + int(time[1]) * 60 + float(time[2])
    elif len(time) == 2:
        time = int(time[0]) * 60 + float(time[1])
    elif len(time) == 1:
        time = float(time[0])
    return time

def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    return "%02d:%02d:%.2f" % (hours, minutes, seconds)

offset = 0.5 ## 默认在视频结尾去除的秒数
fix = 'clip.flv' ## 修复后的文件后缀
fragments = sorted(glob(f'/content/gdrive/Shareddrives/placebo/哔哩哔哩/北京大学/*大学生常见心理问题识别及应对策略*flv'))


def cut_tail(i):
    output = subprocess.getoutput(
        f'''ffmpeg -ss 00:00:00.3 -to 90:02:54.3 -accurate_seek -i "{i}" -codec copy -avoid_negative_ts 1 -y "{i}.{fix}" 2>&1 | grep time= ''')
    duration = re.findall('time=(.*?) ',output)[-1]
    dur = time_convert_ffmpeg(duration)
    dur = dur - offset
    new_dur = seconds_to_time(dur)
    output = subprocess.getoutput(
        f'''ffmpeg -hide_banner -loglevel warning -ss 00:00:00.3 -to {new_dur} -accurate_seek -i "{i}" -codec copy -avoid_negative_ts 1 -y "{i}.{fix}" ''')
    if output:
        print(i,output)

for i in fragments:
    if 'flv.clip.' in i: continue
    output = subprocess.getoutput(
    f'''ffmpeg -hide_banner -loglevel warning -ss 00:00:00.3 -to 90:02:54.3 -accurate_seek -i "{i}" -codec copy -avoid_negative_ts 1 -y "{i}.{fix}" 2>&1''')
    print(output)
    if output:
        print('fix...')
        cut_tail(i)
    print('=====')