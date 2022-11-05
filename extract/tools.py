import requests
from bs4 import BeautifulSoup

from blog.models import Link, Tag

def findAllUrls(link):
    teleLinks=[]
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    atags=soup.find_all("a")
    for i in atags:
        try:
            href=i.attrs['href']
        except:continue
        if(href.find('.me')>0):
            teleLinks.append(href)
            # print(href)
    return teleLinks

def check(url):  # return groupName,groupCount,groupLogo,groupDescri,groupType
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    try:
        groupName = soup.find_all('div', class_="tgme_page_title")[0].get_text().replace("\n", "")        
        groupType="Group"
        if(soup.find_all('div', class_="tgme_page_extra")[0].get_text().find("subscribers")>0):
            groupType = "Channel"
        
    except Exception as e:
        print(e)
        return 0,0,0,0,0,0
    try:
        groupLogo = soup.find_all('img', class_="tgme_page_photo_image")[0]['src']
    except:
        groupLogo = "https://w7.pngwing.com/pngs/419/837/png-transparent-telegram-icon-telegram-logo-computer-icons-telegram-blue-angle-triangle-thumbnail.png"
    try:
        groupCount = soup.find_all('div', class_="tgme_page_extra")[
            0].get_text().split(" subscriber")[0].split(" member")[0]
    except:
        groupCount=0

    try:
        groupDescri = soup.find_all('div', class_="tgme_page_description")[
            0].get_text()
    except:
        groupDescri = groupName+ " help to find your wanted things"

    try:
        groupCount.index("@")
        groupType="Bot"
        groupCount=0
    except:
        pass
    # print(soup.title.text)
    try:
        groupId=soup.title.text.split("@")[1]
    except:
        if(url.find("joinchat")>0):
            groupId=url.split("chat/")[1].replace("/","")
        else:
            groupId=url.split(".me/")[1].replace("/","")
    return groupName, groupCount, groupLogo, groupDescri, groupType,groupId

def addTeleLink(postUrl,categoryId,countryId,languageId,extractData,tags):
    groupName, groupCount, groupLogo, groupDescri, groupType,linkId=extractData
    groupCount=int(str(groupCount).replace(" ",""))
    # print(groupName, groupCount, groupLogo, groupDescri, groupType)

    if(len(Link.objects.filter(linkId=linkId))>0):
        return 

    gtags=[]
    postLink=Link.objects.create(name=groupName,link=postUrl,category=categoryId,language=languageId,country=countryId,description=groupDescri,noOfMembers=groupCount,imgUrl=groupLogo,type=groupType,linkId=linkId)
    spTags = tags.split(",")
    try:
        spTags.remove("")
    except:pass
    for i in spTags:
        try:
            tempTag=Tag.objects.create(name=i)
            gtags.append(tempTag)
        except:
            gtags.append(Tag.objects.get(name=i))
    for i in list(gtags):
        postLink.tag.add(i)
        
def extractUrls(postUrl,categoryId,countryId,languageId,tags):
    teleLinks=findAllUrls(postUrl)
    for i in teleLinks:
        extractData=check(i)
        if(extractData==(0,0,0,0,0,0)):
            continue
        # print(extractData[0] )
        addTeleLink(i,categoryId,countryId,languageId,extractData,tags)


def extractFromGroupSor():
    link = "https://groupsorlink.com/telegram/group/loadresult"
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    inviteBoxs = soup.find_all('div', class_="maindiv")
    print(len(inviteBoxs))
if __name__=="__main__":
    # link="https://www.telegram-groups.com/sinhala-telegram-group/"
    # findAllUrls(link)
    extractFromGroupSor()