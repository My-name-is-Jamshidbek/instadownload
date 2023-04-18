"""
requests
"""
import requests


def request_tiktok(video_link: str, user_id: str):
    """
    :param video_link:
    :param user_id:
    :return:
    """
    url = "http://localhost:8000/tiktok/"
    payload = {"video_global_link": str(video_link), "user_id": user_id}
    response = requests.post(url, json=payload)
    response = response.json()
    return response["video_local_link"]
