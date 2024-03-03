import re
import requests
from bs4 import BeautifulSoup
def check(url):  # return groupName,groupCount,groupLogo,groupDescri,groupType
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    try:
        try:
            groupLink = soup.find_all('a', class_="tgme_username_link")[0].get_text().replace("\n", "")    
        except:
            pass
        
        try:
            groupName = soup.find_all('div', class_="tgme_page_title")[0].get_text().replace("\n", "")    
        except:
            groupName = groupLink.replace("@","").replace("_", " ")
        groupType="Group"
        try:
            if(soup.find_all('div', class_="tgme_page_extra")[0].get_text().find("subscribers")>0):
                groupType = "Channel"
        except:
            groupType = "Unknown"
        
    except Exception as e:
        print(e)
        return 0,0,0,0,0,0
    if groupType == "Unknown":
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

def is_adult_keyword(keyword):
    ADULT_KEYWORDS = ['bokep','adult', 'explicit', '18+', 'nsfw', 'mature', 'XXX','sex', 'sexy','porn','child','onlyfans','masturbating','Baccader','xx']
    for word in ADULT_KEYWORDS:
        if re.search(rf'\b{re.escape(word)}\b', keyword, flags=re.IGNORECASE):
            return True
    return False


if __name__=="__main__":
    # linkg="https://t.me/icolisting"
    # linkg_1="https://t.me/icolisting"
    # linkc='https://t.me/+R26YVj3eW0EzYTc1'
    # links='https://t.me/addstickers/braloveero'
    # linkb='https://t.me/delorean_bot'
    # link_invalid = "https://t.me/bitcoinsrilankar"
    # print(check(linkg))
    # print("/n/n")
    # print(check(linkc))
    # print("/n/n")
    # print(check(links))
    # print("/n/n")
    # print(check(linkb))
    # print("/n/n")
    # print(check(link_invalid))
    print(is_adult_keyword('18+ mature'))