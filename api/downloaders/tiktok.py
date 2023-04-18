"""
tik tok
"""
from TikTokAPI import TikTokAPI


def tiktokdown(video_link):
    """
    :param video_link:
    :return:
    """
    try:
        print(video_link)
        save_path = "videos/tiktok/" + video_link.split("/")[5].split("?")[0] + ".mp4"
        video_id = video_link.split("/")[5].split("?")[0]
        api = TikTokAPI()
        api.downloadVideoById(video_id, save_path)
        return save_path
    except Exception as e:
        print(e)
        return False
