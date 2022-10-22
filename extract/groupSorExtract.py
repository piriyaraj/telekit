import requests
from bs4 import BeautifulSoup

# def extractFromGroupSor():
link = "https://groupsorlink.com/telegram/group/loadresult"
payload={'group_no': 9,'home' : True}
reqs = requests.post(link,data=payload)
soup = BeautifulSoup(reqs.text, 'html.parser')
inviteBoxs = soup.find_all('div', class_="maindiv")
# print(inviteBoxs)
# print(len(inviteBoxs))
for k in range(len(inviteBoxs)):
    box = inviteBoxs[k]
    category = box.find("div",class_="post-basic-info" ).find_all("span")[0].text.replace("\n","")
    country = box.find("div",class_="post-basic-info" ).find_all("span")[1].text.replace("\n","").replace(" ","")
    language = box.find("div",class_="post-basic-info" ).find_all("span")[2].text.replace("\n","").replace(" ","")
    teleLink = "https://t.me/" +box.find("a",class_="joinbtn").attrs["href"].split("popups/")[1]
    tagsTag = box.find_all("a", class_="innertag")
    tags=[]
    for i in tagsTag:
        tags.append(" ".join(i.text.split()))   
    try:
        tags.remove("")
    except:pass
    print("https://groupsorlink.com/telegram/group/invite/"+box.find("a",class_="joinbtn").attrs["href"].split("popups/")[1])
# extractFromGroupSor()[