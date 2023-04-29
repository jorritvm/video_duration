import math
import os
import subprocess
import pandas as pd

# configuration
video_folder_path = r"C:\education\VUB\Algoritmen en datastructuren 2\lectures\recordings"
allowed_extensions = [".mp4"]

# helper functions
def sec2hour(n):
    return math.floor(n / 3600)


def sec2min(n):
    return math.floor((n - sec2hour(n) * 3600) / 60)


def sec2sec(n):
    return n - sec2hour(n) * 3600 - sec2min(n) * 60


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return int(float(result.stdout))


# read the file info
result = dict()
for file in os.listdir(video_folder_path):
    base, ext = os.path.splitext(file)
    full_path = os.path.join(video_folder_path, file)
    if ext in allowed_extensions:
        n = get_length(full_path)
        result[file] = [sec2hour(n), sec2min(n), sec2sec(n), n]

# create a 2D table
df = pd.DataFrame.from_dict(result, orient='index')
df = df.reset_index()
df.shape
df.columns = ["file", "hours", "minutes", "seconds", "total_seconds"]
print(df)

total_seconds = df["total_seconds"].sum()
h,m,s = (sec2hour(total_seconds), sec2min(total_seconds), sec2sec(total_seconds))
total_duration = f"Total time for all movie files is: {h} hours, {m} minutes and {s} seconds."

# export
xls_out_path = os.path.join(video_folder_path, "video_duration.xlsx")
df.to_excel(xls_out_path, index=False)

text_out_path = os.path.join(video_folder_path, "video_duration.txt")
text_file = open(text_out_path, "w")
text_file.write(total_duration)
text_file.close()

print(total_duration)
print("----DONE----")