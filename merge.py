import os
import re
from datetime import datetime,timedelta

PATTERN_INDEX = re.compile(r"^\d{1,3}$" )
PATTERN_TIMESTAMP = re.compile(r"(?P<start>\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2},\d{3})")
PATTERN_EMPTYLINE = re.compile(r"\s*\n")
DELAY = 0.5 # 0.5 second between 2 videos
srts = sorted([file for file in os.listdir() if file.endswith(".srt") and file!="output.srt" ])

offset_index = 0
offset_timestamp = timedelta()
output = []

flag = True # new group start

for srt in srts:
    with open(srt,"r") as f:
        print("[Parsing..]",srt)
        for line in f.readlines():
            index = re.match(PATTERN_INDEX,line)
            timestamp = re.match(PATTERN_TIMESTAMP,line)
            if index:
                if not flag:
                    print("+++++ERROR+++++")
                    print("Gobal index: {} \nLocal index: {}".format(i,index.group()))
                    print(output[-3:])
                    print("+++++ERROR+++++")
                i = int(index.group()) + offset_index
                output.append(str(i)+"\n")
                flag = False
            elif timestamp:
                start = datetime.strptime(timestamp.group("start"),"%H:%M:%S,%f")
                end = datetime.strptime(timestamp.group("end"),"%H:%M:%S,%f")
                start += offset_timestamp
                end += offset_timestamp
                #print(timedelta(seconds=end.second))
                #print("{} {}".format(start,end))
                output.append("{} ---> {}\n".format(start.strftime("%H:%M:%S,%f")[:-3],
                                                    end.strftime("%H:%M:%S,%f")[:-3]))
            elif re.match(PATTERN_EMPTYLINE,line):
                output.append(line)
                flag = True 
            else:
                output.append(line)
                
        offset_index = i
        offset_timestamp = timedelta(hours=end.hour,minutes=end.minute,seconds=end.second+DELAY,microseconds=end.microsecond)

with open("output.srt","w") as f:
    f.writelines(output)
    

