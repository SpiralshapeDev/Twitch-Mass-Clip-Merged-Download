## Required for the script to function
# pip install twitch-dl==2.11.0
# pip install moviepy==2.1.2

import os
import subprocess
import time
import glob
from datetime import date
from moviepy import VideoFileClip, concatenate_videoclips

text_default_color = "\033[0m"
warning_text_color = "\033[93m"

# Get Path
temp_path = str(os.path.abspath(__file__)).replace("app.py","temp/")
print(f"temp path: {temp_path}")

channelName = str(input(f"{text_default_color}Channel Name \n")).lower()
clipRange = str(input(f"{text_default_color}Clip Range (Possible values: last_day, last_week, last_month, all_time) [default: all_time]\n")).lower()
if not ["last_day","last_week","last_month","all_time"].__contains__(clipRange): # By SpiralDev
    print(f"{warning_text_color}[Warning] Couldn't determine time range value " + f'"{clipRange}"' + ', setting to "all_time"')
    clipRange = "all_time"

# Just in case you mistyped something you can cancel.
wait_time = 3
print(f"{text_default_color}Starting download of clips in {wait_time} {("second" if wait_time == 1 else "seconds")}... (max 100 clips)")
time.sleep(wait_time)

subprocess.run(f"twitch-dl clips {channelName} --download --period {clipRange} --target-dir temp")

video_file_list = glob.glob(f"{temp_path}/*.mp4")

loaded_video_list = []

for video in video_file_list:
    print(f"{text_default_color}Adding video file:{video}")
    loaded_video_list.append(VideoFileClip(video))

final_clip = concatenate_videoclips(loaded_video_list)
filename = f"{channelName} {str(date.today()).replace("/","-")} '{clipRange}'.mp4"
final_clip.write_videofile(filename)