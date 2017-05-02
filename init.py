import requests
from bs4 import BeautifulSoup
import os
import errno
import urllib.request
import sys



def getLinks():
    count=1
    url="http://courses.caveofprogramming.com/courses/enrolled/72767"
    source_code=requests.get(url)
    plain_text=source_code.text
    soup=BeautifulSoup(plain_text)
    for links in soup.findAll('div',{'class':'col-sm-12'}):
        divs=links.find('div',{'class':'section-title'})
        divs.find('div',{'class':'section-days-to-drip'}).decompose()
       # print(divs)
        directoryName=cleanDirectoryText(divs.text)
        makeDir(directoryName)

        for ancors in links.findAll('a'):
            href="http://courses.caveofprogramming.com/"+ancors.get('href')
            print(href)
            findDownloadFile(directoryName, href,count)
            count=count+1

def makeDir(dirname):
    try:
        if not os.path.exists(dirname):
            os.mkdir("/home/makusimz/Documents/Python Projects/CaveOfProgramming/"+dirname)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def cleanDirectoryText(directoryName):
    folderName=""
    for word in directoryName:
        if word!=' ':
            folderName=folderName+word

    return  folderName

def findDownloadFile(directory,pageLink,count):
    soup=getSoupObj(pageLink)
    #print(soup)
    videoName = str(count)+" "+getFileName(soup)
    print(videoName)
    #links = soup.find('div', {'class': 'video-options'})
    #print(links)
    downloadLink =soup.find('a',{'class': 'download'}).get('href')
    print(downloadLink)
    #downloadVideo(downloadLink,directory+"/"+videoName)

def downloadVideo(url,videoName):
    link = url
    file_name = videoName
    if(checkifFileExist(file_name)==0):
        with open(file_name, "wb") as f:
            print ("Downloading %s" % file_name)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
    else:
        print("Skipped File "+videoName)
def checkifFileExist(fileName):
    exist=1
    if not os.path.exists(fileName):
        exist=0
    return exist
def getSoupObj(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def getFileName(soupObj):
     name = soupObj.find('h2', {'class': 'section-title'}).text+".avi"
     return name


getLinks()