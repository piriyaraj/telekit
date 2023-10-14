from django.utils import timezone
from datetime import date
import json
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from blog.models import Link, Tag
from django.utils.text import slugify

from blog.views import DiscordNotification

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
        return "already available"

    gtags=[]
    try:
        postLink=Link.objects.create(name=groupName,link=postUrl,category=categoryId,language=languageId,country=countryId,description=groupDescri,noOfMembers=groupCount,imgUrl=groupLogo,type=groupType,linkId=linkId)
    except:
        return 0,0,0,0,0,0
    spTags = tags.split(",")
    try:
        spTags.remove("")
    except:pass
    for i in spTags:
        try:
            tempTag=Tag.objects.create(name=i)
            gtags.append(tempTag)
        except:
            slug=slugify(i)
            gtags.append(Tag.objects.get(slug=slug))
    for i in list(gtags):
        postLink.tag.add(i)
    return "added"
        
def extractUrls(postUrl,categoryId,countryId,languageId,tags):
    teleLinks=findAllUrls(postUrl)
    for i in teleLinks:
        extractData=check(i)
        result=extractData[0]!= 0
        if(extractData==(0,0,0,0,0,0)):
            continue

        result=addTeleLink(i,categoryId,countryId,languageId,extractData,tags)



def extractFromGroupSor():
    link = "https://groupsorlink.com/telegram/group/loadresult"
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    inviteBoxs = soup.find_all('div', class_="maindiv")
    print(len(inviteBoxs))

html_code = """
{% extends "base.html" %} {% load static %}
{% block seo %}
<title>--title--</title>
<meta name="description" content="--description--" />
<meta property="og:description" content="--description--"/>
<meta property="og:title" content="--title--"/>
<meta property="og:image" content="{% static 'images/unlimitedtelegramgroupslinks.webp' %}"/>
<meta name="twitter:image" content="{% static 'images/unlimitedtelegramgroupslinks.webp' %}">
<meta name="robots" content="index, follow" />

<meta property="og:site_name" content="{{ request.get_host }}"/>
<meta property="og:url" content="{{ request.get_host }}{{ request.path }}"/>
<link rel="canonical" href="https://telekit.link{{ request.path }}" />

<meta http-equiv="content-type" content="text/html;charset=UTF-8" />
<meta property="og:locale" content="en_US" />
<meta property="og:type" content="website" />
<meta charset="UTF-8">

<meta name="twitter:card" content="summary_large_image">
{% comment %} <meta name="twitter:site" content="@nytimes"> {% endcomment %}
<meta name="twitter:title" content="--title--">
<meta name="twitter:description" content="--description--">
{% endblock %}
{% block content %}
<div class="content">
  <div class="wrap">
    <div id="main" role="main">
        <h1>--title--</h1>
        <img src="{% static 'images/unlimitedtelegramgroupslinks.webp' %}" alt="Unlimited Telegram groups and channels links" title="Unlimited Telegram groups and channels links">
        <div>--context--</div>
        <p>Welcome to the ultimate guide to thousands of <b>active Telegram groups links</b> ! Telegram is a popular messaging app with millions of users around the world, and joining groups is a great way to connect with people who share your interests. In this guide, we have compiled a list of over 10,000 active Telegram groups that cover a wide range of topics, from <b>entertainment</b> to <b>education</b>, from <b>sports</b> to <b>politics</b>. Whether you're looking for a group to chat with friends or to learn new skills, you're sure to find one that suits your needs. So <b>join</b>, <b>share</b>, and <b>submit</b> your own Telegram group links to become part of this vibrant community!</p>
        --table--
    </div>
  </div>
</div>
{% endblock %}

"""

def createATable(tableTitle, colHeading1, colHeading2, col1Data, col2Data, article = ""):
    # Create the opening HTML tags for the table
    html = "<br></br> <hr> <h2 id='{}'>{}</h2><br/>{}<br/><table>".format(tableTitle.replace(" ","-").replace("/","-"),tableTitle,article)
    
    
    
    # Create the table headers
    html += "<tr><th>{}</th><th>{}</th></tr>".format(colHeading1, colHeading2)
    
    # Create the table rows and data
    for i in range(len(col1Data)):
        html += "<tr><td>{}</td><td><a class='linkbutton' href='{}'>Join</a></td></tr>".format(col1Data[i], col2Data[i])
        
    # Create the table caption
    head = tableTitle.split("telegram")[0]
    html += "<caption><b>{}</b> telegram group links</caption>".format(head)
    
    # Create the closing HTML tags for the table
    html += "</table>"
    # html += article
    
    return html

def createHtmlPage():
    global html_code
    tempHtml = """"""
    tempContext = """
        <div id="toc_container">
        <p class="toc_title">Contents</p>
        <ul class="toc_list">
        ^
        </ul>
        </div>
    """
    country = []
    language = []
    category = []
    postLink=Link.objects.filter()
    title = str(len(postLink))+"+ Active Telegram Groups Links |Join, Submit|"+str(date.today().strftime("%d %b %Y"))
    description = "Join 10,000+ Active popular Telegram groups Links in "+str(date.today().strftime("%Y"))+" | join and Share telegram groups and channels. Find most top category links on telekit"

    with open('pageMaker.json', 'r', encoding='utf-8') as file:
    # Load the contents of the file into a variable
        data = json.load(file)
    with open('article.json', 'r', encoding='utf-8') as file:
    # Load the contents of the file into a variable
        article = json.load(file)
        
    for key in data:
        if key['model'] == "blog.language":
            language.append(key["fields"]["name"])
        elif key['model'] == "blog.country":
            country.append(key["fields"]["name"])
        elif key['model'] == "blog.category":
            category.append(key["fields"]["name"])

    for i in category+language+country:
        links = Link.objects.filter(Q(category__name=i) | Q(language__name=i) | Q(country__name=i)).order_by('-added')[:10]
        if(len(links)):
            name = []
            groupLink = []
            for link in links:
                name.append(link.name)
                groupLink.append(f"/join/{link.linkId}")
            # print(article[i])
            id = (i+" telegram groups links").replace(" ","-").replace("/","-")
            tempContext = tempContext.replace("^",f'<li><a href="#{id}">{i+" telegram groups links" }</a></li>\n^')
            tempHtml += createATable(i+" telegram groups links",i+" group name","Links",name, groupLink, article[i])
    html_code = html_code.replace("--context--",tempContext)
    html_code = html_code.replace("--table--",tempHtml)
    html_code = html_code.replace("--title--",title)
    html_code = html_code.replace("--description--",description)
    with open('templates/blog/seoTest1.html', 'w', encoding='utf-8') as file:
    # Write the HTML code to the file
        file.write(html_code)

def removeInvalidurl():
    # result = check("https://t.me/audrius_baciulis")
    # # result = check("https://t.me/+YSLzPmSjzeM3MWJl") #revoked
    # # result = check("https://telegram.me/apkmodultra") #revoked
    # print(result)
    # return " hello "
    removedLink = ""
    first_links = Link.objects.order_by('modified')[:100]
    count = 0
    for linkObj in first_links:
        try:
            # # return groupName,groupCount,groupLogo,groupDescri,groupType
            extractData = check(linkObj.link)
            
            if extractData == (0, 0, 0, 0, 0, 0):
                # delete linkObj
                linkObj.delete()
                removedLink += linkObj.link+"   "
                count += 1
            else:
                linkObj.name = extractData[0]
                linkObj.noOfMembers = 1
                linkObj.description = extractData[3]
                linkObj.type = extractData[4]
                linkObj.save()
                linkObj.noOfMembers = int(extractData[1].replace(" ",""))
                linkObj.save()

        except Exception as e:
            DiscordNotification(f"Telekit: An error occurred for link ID {linkObj.link}: {str(e)}")
            
            # Handle exceptions here, you can print or log the error
            print(f"An error occurred for link ID {linkObj.id}: {str(e)}")
            continue
    DiscordNotification(f"Telekit: Out of {len(first_links)} links, {count} removed links: {removedLink}")
    return f"Out of {len(first_links)} links, {count} removed"

# Replace 'check' with the actual function you're using to validate links


if __name__=="__main__":
    # link="https://www.telegram-groups.com/sinhala-telegram-group/"
    # findAllUrls(link)
    createHtmlPage()