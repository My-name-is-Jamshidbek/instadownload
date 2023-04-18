"""
main
"""
from fastapi import FastAPI
from pydantic import BaseModel
from downloaders.tiktok import tiktokdown

app = FastAPI()


class Tiktok(BaseModel):
    """
    tik tok
    """
    video_global_link: str


@app.post("/tiktok/")
async def create_item(tiktok: Tiktok):
    """
    :param tiktok:
    :return:
    """
    tiktok_dict = tiktok.dict()
    video_local_link = tiktokdown(tiktok_dict["video_global_link"])
    if video_local_link:
        tiktok_dict = {"video_local_link": video_local_link}
    else:
        tiktok_dict = {"video_local_link": "False"}
    return tiktok_dict
