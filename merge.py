import os
import re
from datetime import datetime,timedelta

PATTERN_INDEX = re.compile(r"^\d{1,3}$" )
PATTERN_TIMESTAMP = re.compile(r"(?P<start>\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2},\d{3})")
PATTERN_EMPTYLINE = re.compile(r"\s*\n")

manual_offset_between2vid = 0.5 # 0.5 second between 2 videos
manual_offset_between2sub = 10 # 10 ms between 2 sub



def parse(srts):
    offset_timestamp = timedelta()
    output = []
    isfirst = True 
    _type = "INDEX"
    for srt in srts:
        with open(srt,"r") as f:
            print("[Parsing..]",srt)
            for line in f.readlines():
                index = re.match(PATTERN_INDEX,line)
                timestamp = re.match(PATTERN_TIMESTAMP,line)
                if index and not isfirst:
                    output.append((shifted_timestamp.strip(),sub.strip())) # save prev group and remove \n
                    _type = "INDEX"
                    i = index.group()
                elif timestamp:
                    start = datetime.strptime(timestamp.group("start"),"%H:%M:%S,%f")
                    end = datetime.strptime(timestamp.group("end"),"%H:%M:%S,%f")
                    start += offset_timestamp
                    end += offset_timestamp
                    shifted_timestamp = ("{} ---> {}\n".format(start.strftime("%H:%M:%S,%f")[:-3],
                                                        end.strftime("%H:%M:%S,%f")[:-3]))
                    _type = "TIMESTAMP"
                elif re.match(PATTERN_EMPTYLINE,line):
                    pass
                else:
                    # if there are multiple lines of subtitle, only the last line will be collected
                    # this is to address the issue that before CN-sub there is a EN-sub accidentally lefted here.
                    # For now we will only generate a warning.
                    if _type == "SUB":
                        print("[Warning] Subtitle overwrite!!! @{}".format(i))
                        print("Relpaced by",line) # if print CN-sub, you dont need to fix it.
                    sub = line 
                    isfirst = False
                    _type = "SUB"
            output.append((shifted_timestamp.strip(),sub.strip())) # save last group and remove \n
            # save the end timestamp of last srt file. it will be the offset of next one
            offset_timestamp = timedelta(hours=end.hour,
                                                                        minutes=end.minute,
                                                                        seconds=end.second+manual_offset_between2vid, 
                                                                        microseconds=end.microsecond+manual_offset_between2sub)
    return output
    
def main():
    srts = [file for file in os.listdir() if file.endswith(".srt") and file!="output.srt" ]
    srts.sort(key=lambda x:int(x.split("-")[0]))

    output = parse(srts)
    with open("output.srt","w") as f:    
        for index,item in enumerate(output):
            f.write(str(index+1)+"\n")
            f.write(item[0]+"\n")
            f.write(item[1]+"\n\n")


if __name__ == "__main__":
    main()