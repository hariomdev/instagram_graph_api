from fastapi import FastAPI
import aiohttp, os, requests, boto3
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Union
import config as aws_credentials

"""LOAD ENVIRONMENT VARIABLES"""
load_dotenv()

"""CREATE FastAPI CLASS INSTANCE """
app = FastAPI()
URL = os.getenv("BASE_URL")
ig_user_id = os.getenv('IG_USER_ID')
media_id = os.getenv('MEDIA_ID')

# s3 bucket connection
s3 = boto3.resource(
    service_name= aws_credentials.SERVICE_NAME,
    region_name=aws_credentials.DEFAULT_REGION_NAME,
    aws_access_key_id=aws_credentials.AWS_ACCESS_KEY,
    aws_secret_access_key=aws_credentials.AWS_SECRET_KEY
)

# All reuired parameters for the instagram graph api
params = {'access_token' : os.getenv("ACCESS_TOKEN")}

video_param = {
    'access_token' : os.getenv("ACCESS_TOKEN"),
    'media_type' : 'VIDEO',
    'video_url' : 'https://twitter.com/googledevs/status/1615408660276039680'
    }

media_meta_data = {
    'access_token' : os.getenv("ACCESS_TOKEN"),
    'fields' : 'id,media_type,media_url,owner,timestamp,caption,comments_count,ig_id,is_comment_enabled,is_shared_to_feed,like_count,media_product_type,permalink,shortcode,thumbnail_url,username'
}


"""all web route"""
@app.get("/")
async def get_current_accounts():
    async with aiohttp.ClientSession() as session:
        # async with session.get(URL) as resp:
        async with session.get(url=URL+'me/accounts/', params=params) as resp:
            data = await resp.json()
            return data

@app.get("/get_all_media/")
async def get_media():
    async with aiohttp.ClientSession() as session:
        # async with session.get(URL) as resp:
        async with session.get(url=URL+ig_user_id+'/media', params=params) as resp:
            data = await resp.json()
            return data

"""request body"""
class post_ig_video_body(BaseModel):
    media_type : str
    video_url : str
    is_carousel_item : Union[bool, None] = None
    caption : Union[str, None] = None
    location_id : Union[str, None] = None
    thumb_offset : Union[str, None] = None
    product_tags : Union[str, None] = None

data=post_ig_video_body.schema_json()

@app.get("/post_reel/")
async def post_ig_reel():
    async with aiohttp.ClientSession() as session:
        # async with session.get(URL) as resp:
        async with session.post(url=URL+ig_user_id+'/media', params=video_param) as resp:
            data = await resp.json()
            return data



@app.get("/get_media_meta_data/")
async def get_media_data():
    async with aiohttp.ClientSession() as session:
        # async with session.get(URL) as resp:
        async with session.get(url=URL+media_id, params=media_meta_data) as resp:
            data = await resp.json()
            print(data['permalink'])
            video_url = requests.get(data['permalink'], stream=True, headers={'Accept-Encoding': None})
            size = video_url['Content_Length']
            count_score = size+data['comments_count']+data['like_count']
            return data


# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: body, q: Union[str, None] = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result