from glob import glob
import os

allFpath = sorted(glob(f'/content/gdrive/Shareddrives/placebo/哔哩哔哩/北京大学/*古今春节民俗文化*flv'))
output = "/content/gdrive/Shareddrives/placebo/哔哩哔哩/古今春节民俗文化_北京大学_20220111_ts.mp4"

cmd=""
s_ts = "concat:"
for i in allFpath[:]:
    temp = f'ffmpeg -i "{i}" -c copy -bsf:v h264_mp4toannexb -f mpegts "{i}.ts"'
    print(temp)
    cmd += temp+'\n'
    s_ts += f'{i}.ts|'

temp = f'ffmpeg -i "{s_ts[:-1]}" -c copy -bsf:a aac_adtstoasc "{output}"'
print(temp)
cmd += temp+'\n'

print()

os.system(cmd)