import subprocess,os
from glob import glob

datekw = '2021-04-11'
kw = "古今春节民俗文化"
room = "北京大学"
date= datekw.replace('-','')#"202103"
fix= '' ## 用来判断拿不拿修复后的片段合并
## Windows
# path_prefix = f'D:/TMP/成电/' 
## linux_colab
path_prefix = f'/content/gdrive/Shareddrives/placebo/哔哩哔哩/{room}/' 
path = f'{path_prefix}*{datekw}*{kw}*{fix}.flv'
allpath = sorted(glob(path))

## 检查分辨率
for i in allpath:
    print(i[i.rfind('/'):], end=' ')
    os.system(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{i}"')

## 生成待合并的文件列表
sum = 0
with open('concat.txt', 'w') as f:
    for i in allpath:#08-12* +
        print(i, os.stat(i).st_size)
        sum += os.stat(i).st_size
        f.write(f"file '{i}'\n")
print(sum)

## 执行合并操作
cmd = ["ffmpeg","-analyzeduration", "2147483647", "-probesize", "2147483647", "-y", "-f", "concat", "-safe", '0', "-i", 'concat.txt', '-c', 'copy', 
       f'D:/TMP_ggyun/{kw}_{room}_{date}.flv'] ##
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) #["ls","-lha"]
output, errors = p.communicate()
print(output,errors)