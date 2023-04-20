import asyncio
import io
import glob
import os
import subprocess
import urllib.request
from os import path
from urllib import request

import aiohttp
from tiktokapipy.async_api import AsyncTikTokAPI
from tiktokapipy.models.video import Video
from TikTokApi import TikTokApi

directory = ""
url = 'https://www.tiktok.com/@galaxykidrage/video/7221672357939793154?is_from_webapp=1&sender_device=pc'
def save_slideshow(video):
    # this filter makes sure the images are padded to all the same size
    vf = "\"scale=iw*min(1080/iw\,1920/ih):ih*min(1080/iw\,1920/ih)," \
         "pad=1080:1920:(1080-iw)/2:(1920-ih)/2," \
         "format=yuv420p\""

    for i, image_data in enumerate(video.image_post.images):
        url = image_data.image_url.url_list[-1]
        # this step could probably be done with asyncio, but I didn't want to figure out how
        urllib.request.urlretrieve(url, path.join(directory, f"temp_{video.id}_{i:02}.jpg"))

    urllib.request.urlretrieve(video.music.play_url, path.join(directory, f"temp_{video.id}.mp3"))

    # use ffmpeg to join the images and audio
    command = [
        "ffmpeg",
        "-r 2/5",
        f"-i {directory}/temp_{video.id}_%02d.jpg",
        f"-i {directory}/temp_{video.id}.mp3",
        "-r 30",
        f"-vf {vf}",
        "-acodec copy",
        f"-t {len(video.image_post.images) * 2.5}",
        f"{directory}/temp_{video.id}.mp4",
        "-y"
    ]
    ffmpeg_proc = subprocess.run(
        " ".join(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    _, stderr = ffmpeg_proc.communicate()

    generated_files = glob.glob(path.join(directory, f"temp_{video.id}*"))

    if not path.exists(path.join(directory, f"temp_{video.id}.mp4")):
        # optional ffmpeg logging step
        # logging.error(stderr.decode("utf-8"))
        for file in generated_files:
            os.remove(file)
        raise Exception("Something went wrong with piecing the slideshow together")

    with open(path.join(directory, f"temp_{video.id}.mp4"), "rb") as f:
        ret = io.BytesIO(f.read())

    for file in generated_files:
        os.remove(file)

    return ret


def save_video(video):
    with request.get(video.video.download_addr) as resp:
        return io.BytesIO(resp.content)


def download_video(link):
    TikTokApi._browser = None
    TikTokApi._clean_up = None
    # mobile emulation is necessary to retrieve slideshows
    # if you don't want this, you can set emulate_mobile=False and skip if the video has an image_post property
    with TikTokApi(emulate_mobile=True, _browser=None) as api:
        video = api.get_video_by_url(link)
        if video.image_post:
            downloaded = save_slideshow(video)
        else:
            downloaded = save_video(video)

    return downloaded

download_video(link=url)