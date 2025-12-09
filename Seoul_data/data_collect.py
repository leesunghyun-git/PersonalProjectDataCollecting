import requests as req
import pymysql as db
import numpy as np
import pandas as pd
import time
REST_API_KEY = "dbda976eb054714809926c699703fc3b"
conn= db.connect(
    host="127.0.0.1",
    user="root",
    password="Simple645*",
    database="mydb",
    port=3306,
    charset="utf8mb4"
)
cur = conn.cursor()
url ="https://dapi.kakao.com/v2/local/search/category.json"
headers = {"Authorization": f"KakaoAK {REST_API_KEY}"}
def generate_grid_points(center_lat, center_lng, grid_km=1, grids=3):
    # 1km 기준 위도/경도 오프셋
    lat_offset = 0.009 * grid_km
    lng_offset = 0.011 * grid_km

    mid = grids // 2
    points = []

    for i in range(grids):
        for j in range(grids):
            lat = center_lat + (i - mid) * lat_offset
            lng = center_lng + (j - mid) * lng_offset
            points.append((lat, lng))
    return points

seoul_gu_centers = {
    "강남구": (37.517236, 127.047325),
    "강동구": (37.530126, 127.123770),
    "강북구": (37.639937, 127.025508),
    "강서구": (37.550937, 126.849533),
    "관악구": (37.478406, 126.951613),
    "광진구": (37.538484, 127.082293),
    "구로구": (37.495485, 126.858121),
    "금천구": (37.456872, 126.895197),
    "노원구": (37.654258, 127.056680),
    "도봉구": (37.668768, 127.047163),
    "동대문구": (37.574371, 127.040679),
    "동작구": (37.512402, 126.939252),
    "마포구": (37.566324, 126.901491),
    "서대문구": (37.579115, 126.936778),
    "서초구": (37.483712, 127.032411),
    "성동구": (37.563341, 127.036373),
    "성북구": (37.589400, 127.016749),
    "송파구": (37.514563, 127.105918),
    "양천구": (37.516028, 126.866657),
    "영등포구": (37.526371, 126.896228),
    "용산구": (37.532600, 126.990898),
    "은평구": (37.617612, 126.922700),
    "종로구": (37.573050, 126.979189),
    "중구": (37.563646, 126.997565),
    "중랑구": (37.606320, 127.092584),
}
seoul_gu=[
  (37.517236, 127.047325,5),
  (37.530126, 127.123770,3),
  (37.639937, 127.025508,4),
  (37.550937, 126.849533,5),
  (37.478406, 126.951613,4),
  (37.538484, 127.082293,3),
  (37.495485, 126.858121,4),
  (37.456872, 126.895197,3),
  (37.654258, 127.056680,5),
  (37.668768, 127.047163,4),
  (37.574371, 127.040679,3),
  (37.512402, 126.939252,3),
  (37.566324, 126.901491,4),
  (37.579115, 126.936778,3),
  (37.483712, 127.032411,5),
  (37.563341, 127.036373,3),
  (37.589400, 127.016749,4),
  (37.514563, 127.105918,5),
  (37.516028, 126.866657,3),
  (37.526371, 126.896228,4),
  (37.532600, 126.990898,3),
  (37.617612, 126.922700,4),
  (37.573050, 126.979189,3),
  (37.563646, 126.997565,3),
  (37.606320, 127.092584,3)
]
category_code = ["CE7","FD6","AD5","AT4","CT1","MT1","CS2"]

category_table = {
   "CE7" : "cafe",
   "FD6" : "food",
   "AD5" : "lodging",
   "AT4" : "attraction",
   "CT1" : "culture",
   "MT1" : "mart",
   "CS2" : "cstore"
}
result =[]
# print(category_code[0])
# params={
#   'category_group_code' : category_code[0],
#   'x':'127.901491',
#   'y':'37.566324',
#   'radius':2000,
#   'page':1,
#   'size':15
# }
# res = req.get(url,params=params,headers=headers)

# data=res.json()
# print(data)
cat_index = 0
gu_index = 0
for i in range (1,701):
  print(f'{i}번째 데이터 파싱')
  (y,x,grid)=seoul_gu[gu_index]
  pointgrid = generate_grid_points(y,x,grids=grid)
  for j in range (len(pointgrid)):
    (y,x) = pointgrid[j]
    l = 1
    while True :
      params={
      'category_group_code' : category_code[cat_index],
      'x':x,
      'y':y,
      'radius':2000,
      'page':l,
      'size':15
      }
      res = req.get(url,params=params,headers=headers)
      data = res.json()
      result.append(data['documents'])
      if data['meta']['is_end']==True:
        break
      else:
        l+=1
        time.sleep(0.3)
  gu_index+=1
  if gu_index == len(seoul_gu):
    gu_index=0
    cat_index+=1
  if cat_index == len(category_code):
    break
