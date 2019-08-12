import requests
import os, time
import telegram

from bs4 import BeautifulSoup

bot = telegram.Bot(token = 'IOW7fab-il-5iDEGJmux8Q3VoOY')
chatID = '@redtea_bot'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEATIME_FILE_NAME = "teaTimeLatest.txt"
TIMELINE_FILE_NAME = "timeLineLatest.txt"
GREETING_FILE_NAME = "greetingLatest.txt"
FUN_FILE_NAME = "funLatest.txt"

def writeFile(fileName, message):
    with open(os.path.join(BASE_DIR, fileName), 'w+') as fileWrite:
        fileWrite.write(message)
        fileWrite.close()

def readFileAndUpdate(fileName, latest, message):
    with open(os.path.join(BASE_DIR, fileName), 'r+') as fileRead:
        before = fileRead.readline()

        if before != latest:
            bot.sendMessage(chat_id = chatID, text=message)
        
        fileRead.close()


def updateTimeLine():
    timeLineReq = requests.get('http://redtea.kr/pb/pb.php?id=timeline')
    timeLineHtml = timeLineReq.text
    
    soup = BeautifulSoup(timeLineHtml, 'html.parser')
    postDate = soup.select('input.cmtfold')

    datanum = postDate[1].get('id')[3:]
    print(datanum)
    latest = datanum[1]

    with open(os.path.join(BASE_DIR, TIMELINE_FILE_NAME), 'r+') as fileRead:
        before = fileRead.readline()
        print(before)
        if before != latest and (int(latest) - int(before) == 0):
            bot.sendMessage(chat_id = chatID, text= latest - before + "개의 새 타임라인 글이 있습니다.")
        
        fileRead.close()
    writeFile(TIMELINE_FILE_NAME,latest)


def updateTeaTime():  
    teaTimeReq = requests.get('http://redtea.kr/pb/pb.php?id=free')
    teaTimeHtml = teaTimeReq.text

    soup = BeautifulSoup(teaTimeHtml, 'html.parser')

    postDate = soup.select('td.tdnum')
    postTitle = soup.select('span.subj')

    latest = postDate[1].text

    readFileAndUpdate(TEATIME_FILE_NAME, latest, postTitle[1].text + " http://redtea.kr/pb/pb.php?id=free&no=" + latest)
    writeFile(TEATIME_FILE_NAME,latest)

def updateGreeting():
    greeTingReq = requests.get('http://redtea.kr/pb/pb.php?id=greeting')
    greeTingHtml = greeTingReq.text

    soup = BeautifulSoup(greeTingHtml, 'html.parser')

    postDate = soup.select('td.tdnum')

    latest = postDate[1].text

    readFileAndUpdate(GREETING_FILE_NAME, latest, "새로운 가입자가 있습니다. http://redtea.kr/pb/pb.php?id=greeting&no=" + latest)
    writeFile(GREETING_FILE_NAME,latest)

def updateHumor():
    funReq = requests.get('http://redtea.kr/pb/pb.php?id=fun')
    funHtml = funReq.text

    soup = BeautifulSoup(funHtml, 'html.parser')

    postDate = soup.select('td.tdnum')

    latest = postDate[1].text

    readFileAndUpdate(FUN_FILE_NAME, latest, "새로운 유머 글이 있습니다. http://redtea.kr/pb/pb.php?id=fun&no=" + latest)
    writeFile(FUN_FILE_NAME,latest)

while True:
    #updateTimeLine()
    updateTeaTime()
    updateGreeting()
    updateHumor()

    time.sleep(60)
