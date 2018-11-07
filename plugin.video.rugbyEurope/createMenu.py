import urllib2, xbmc
from bs4 import BeautifulSoup

GAMES = 'https://www.rugbyeurope.eu/welcome-rugby-europe-tv'
ICON = 'https://upload.wikimedia.org/wikipedia/ro/a/a0/Rugby_Europe_logo.png'
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.rugbyEurope')

def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try: 
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except: pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link

def GetVideoId(url):
    html = Open_Url('https://www.rugbyeurope.eu/'+url)
    soup = BeautifulSoup(html,"html.parser")
    video = soup.find('iframe')
    try:
      videoLink = video.get('src')
      return videoLink[34:]
    except: 
      return "error"

def GetDescription(url):    
    html = Open_Url('https://www.rugbyeurope.eu/'+url)
    soup = BeautifulSoup(html,"html.parser")
    description = soup.find('div',{'class':'place'})
    try:
      return description.text
    except: 
      return "error"

def CreateStrm(videoId):
    url = "plugin://plugin.video.dailymotion_com/?url=%s&mode=playVideo"%videoId
    path = '%s/strmFiles/%s.strm'%(ADDON_PATH,videoId)
    f = open(path,'w+')
    f.write('%s\n'%url)
    f.close()
 

def CreateGamesMenu():
    f = open(ADDON_PATH+'/menu.php','w+')

    html = Open_Url(GAMES)
    soup = BeautifulSoup(html,"html.parser")
    content =  soup.find('div', {'class':'container collapsed'})
    for game in content.find_all('a',class_="bk-web-tv"):
      title = game.find('div',{'class':'title'})
      img = game.find('img').get('src')
      link = game.get('href')
      videoId = GetVideoId(link)
      #description = GetDescription(link)
      CreateStrm(videoId)
      f.write("<NAME>%s</NAME><URL>%s/strmFiles/%s.strm</URL><ICON>%s</ICON><FANART>%s</FANART><DESC> </DESC>"% (title.text,ADDON_PATH,videoId,img,ICON))
    f.close()

CreateGamesMenu()