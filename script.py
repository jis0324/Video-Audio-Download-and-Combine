import os
import csv
import ffmpeg
import requests

base_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = base_dir + '/download/'
result_dir = base_dir + '/result/'

# /* Make download folder */
if not os.path.exists(download_dir):
  os.makedirs(download_dir)

# /* Make result folder */
if not os.path.exists(result_dir):
  os.makedirs(result_dir)

# /* Get Video & Audio List */
urls_data = list()
with open(base_dir + '/urls.csv') as urls_csv:
  urls_data = list(csv.DictReader(urls_csv))

for url_item in urls_data:
  try:
    # /* DownLoad Video & Audio List */
    print("Video Path : ", url_item["Video_URL"])
    print("Downloading Video...")
    video_request = requests.get(url_item["Video_URL"])
    video_file = download_dir + 'video.' + url_item["Video_URL"].rsplit('.', 1)[1]
    open(video_file, 'wb').write(video_request.content)

    print("Audio Path : ", url_item["Audio_URL"])
    print("Downloading Audio...")
    audio_request = requests.get(url_item["Audio_URL"])
    audio_file = download_dir + 'audio.' + url_item["Audio_URL"].rsplit('.', 1)[1]
    open(audio_file, 'wb').write(video_request.content)

    # /* Combine Video & Audio List */
    print("Combining Video and Audio...")
    video_stream = ffmpeg.input(video_file)
    audio_stream = ffmpeg.input(audio_file)
    ffmpeg.output(audio_stream, video_stream, result_dir + url_item["Result_Name"]).run()

    os.remove(video_file)
    os.remove(audio_file)
    print('END!')
  except Exception as err:
    print(err)
    continue