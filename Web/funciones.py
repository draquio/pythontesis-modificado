from Web.db import get_db
from flask import request
from bs4 import BeautifulSoup
import mysql.connector
import time, atexit, requests, random
from apscheduler.schedulers.background import BackgroundScheduler
from apiclient.discovery import build
youtube = build('youtube', 'v3', developerKey="AIzaSyDadJbuTMoB_wExqYvFtQppynh6sgMM3GI")



    



def ScrapClimaSemanal():
    url = requests.get("https://www.tutiempo.net/yacuiba.html")
    soup = BeautifulSoup(url.text, 'html.parser').find('div', class_="tiledias").find_all('span', class_="t max")


def ScrapClimaHoy():
  url = requests.get("https://www.tutiempo.net/tarija.html")
  soup = BeautifulSoup(url.text, 'html.parser')
  soup = soup.find('div', class_="tiledias").find('td', class_="tiledia-1 first sel").find('span', class_="t max")
  climaennumero = soup.text.split("°")
  climaactual = int(climaennumero[0])
  print("el clima es {} a la hora {}".format(climatotal, time.strftime("%H:%M %p")))


def PromedioClimaSemanal():
    url = requests.get("https://www.tutiempo.net/yacuiba.html")
    soup = BeautifulSoup(url.text, 'html.parser')
    soup = soup.find('div', class_="tiledias")
    soup = soup.find_all('span', class_="t max")
    i = 0
    total = 0
    for item in soup:
        climaennumero = soup[i].text.split("°")
        total = total+int(climaennumero[0])
        i = i+1
    aux = int(total/7)
    total = str(aux)
    print(total)
    return total

#Buscar Video de youtube
def searchVideoQuery(query,youtube,relevancia):
  busqueda = query+" receta"
  videos = []
  pageToken=''
  search_response = youtube.search().list(
  q=busqueda,
  part="id,snippet",
  type="video",
  order=relevancia,
  pageToken=pageToken,
  videoEmbeddable="true",
  maxResults=9
  ).execute()
  pageToken=search_response.get("nextPageToken")
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  
  return videos

#Mostrar video en específico
def mostrar_video(youtube, v_id):
  videos = youtube.videos().list(
    id=v_id,
    part="id,snippet",
  ).execute()
  if not videos["items"]:
    # print("Video '%s' was not found." % v_id)
    sys.exit(1)
  video = videos["items"][0]["snippet"]
  return video





# -------------- Cron --------------  
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=ScrapClimaSemanal, trigger="interval",  minutes=10)
# scheduler.add_job(ScrapClimaHoy, 'cron', minute='1-59')
# scheduler.add_job(print_date_time, 'cron', minute='1-59')
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
# print(climatotal)

# -------------- Fin Cron -------------- 
