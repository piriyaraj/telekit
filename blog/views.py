from ast import keyword
from email import message
from multiprocessing import context
from os import link
import random
from re import L
import re
from unicodedata import category
from unittest import result
from wsgiref.util import request_uri
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from blog.models import Category, Company, Country, Language, Link, Tag
# from extract.models import Notification
from . import tools
from django.core.paginator import Paginator
from datetime import date


def pagination(request,obj):
    paginator = Paginator(obj, 6) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    linka = paginator.get_page(page_number)
    return linka

def links(request,path,message={}):
    postLink=Link.objects.filter(linkId=path)[0]
    country=postLink.country
    language=postLink.language
    category=postLink.category
    relatedLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot"),country=country, language=language, category=category).order_by("-id")
    relatedLink=relatedLink.exclude(id=postLink.id)
    showAds=postLink.category.name=="Adult/18+/Hot"
    
    if(request.GET.get('page')):
        linka = pagination(request, relatedLink)
        context = {
            'links': linka,
        }
        if(showAds):
            context["adsshow"]=True
        return render(request, "loadmore.html", context)

    linka = pagination(request, relatedLink)
    seo = {
        'title': "Join Active "+postLink.name+" Telegram "+postLink.type+" | Find the Latest Invite Link "+str(date.today().year),
        "description": "Join active "+postLink.name+" Telegram "+postLink.type+" with ease. Discover what makes this "+postLink.type+" unique and engage with fellow members. Check out our blog for the latest invite link and start exploring today!",
        "robots": "index, follow",
        "ogimage": postLink.image_file.url,
    }
    context={
        "post":postLink,
        "links": linka,
        'seo':seo,
        "article":f'''
        <div>
	<div>
		<p>If you're looking for a new community to join on Telegram, we've got just the one for you! Introducing {postLink.name}, a {postLink.category} {postLink.type} from {postLink.country } with {postLink.noOfMembers} members.</p>
		<p>To join {postLink.name}, simply click on the link provided. {postLink.type} links are a great way to stay connected with like-minded individuals from around the world.</p>
		<p>The {postLink.language} language is primarily used in this {postLink.type}, making it the perfect place for speakers of this language to come together and engage in discussions on various topics.</p>
		<p>The {postLink.tag} tag is used to describe the {postLink.type}'s interests and can give you a better idea of what to expect when you join.</p>
		<p>In {postLink.name}, you'll find a diverse group of individuals who are passionate about {postLink.description}. Whether you're looking for a place to share your thoughts, ask for advice, or simply connect with others, you'll find a welcoming community in {postLink.name}.</p>
		<p>So what are you waiting for? Click on the link to join {postLink.name} today and start connecting with like-minded individuals from around the world.</p>
	</div>
	<div>
		<p>If you're looking for a new community to join on Telegram, we've got just the one for you! Introducing {postLink.name}, a {postLink.category} {postLink.type} from {postLink.country} with {postLink.noOfMembers} members.</p>
		<p>To join {postLink.name}, simply click on the link provided. {postLink.type} links are a great way to stay connected with like-minded individuals from around the world.</p>
		<p>The {postLink.language} language is primarily used in this {postLink.type}, making it the perfect place for speakers of this language to come together and engage in discussions on various topics.</p>
		<p>The {postLink.tag} tag is used to describe the {postLink.type}'s interests and can give you a better idea of what to expect when you join.</p>
		<p>In {postLink.name}, you'll find a diverse group of individuals who are passionate about {postLink.description}. Whether you're looking for a place to share your thoughts, ask for advice, or simply connect with others, you'll find a welcoming community in {postLink.name}.</p>
		<p>So what are you waiting for? Click on the link to join {postLink.name} today and start connecting with like-minded individuals from around the world.</p>
	</div>
 </div>
'''
        
    }
    if(showAds):
        context["adsshow"]=True
    context.update(message)
    return render(request,"links.html",context)

def index(request):
    link=Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot")).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,link)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo={
        'title': f"1500+ Active telegram groups links List - {date.today().month}/{date.today().year}",
        "description": "1500+ links to unlimited Telegram groups and channels Add your Telegram links here as well to boost the Telegram growth factor.",
        "robots":"index, follow"
    }
    linka=pagination(request,link)
    
    context={
      'links':linka,
      'seo':seo,
    }
    return render(request, "index.html",context)
    
def loadmore(request):
    # link=Link.objects.order_by("-id")
    linka=pagination(request,link)
    context={
      'links':linka,
    }
    return render(request,"loadmore.html",context)

def docfiles(request,path):
    file="doc/"+path+".html"
    seo = {
        'title': "Telekit "+path+" page",
        "description": "Telekit "+path+" provide all information about "+path+".",
        "robots": "index, nofollow"
    }
    return render(request,file,{"seo":seo})


def groupfiles(request, path, message={}):
    seo = {
        'title': "Telekit "+path+" page",
        "description": "Telekit "+path+" provide all information about "+path+".",
        "robots": "index, nofollow"
    }
    file="group/"+path+".html"
    context={
        "seo":seo
    }
    context.update(message)
    return render(request, file, context)


def category(request,path):
    showAds=True
    cate=Category.objects.get(slug=path)
    if(cate.name!="Adult/18+/Hot"):
        postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot"),category=cate).order_by("-id")
    else:
        postLink = Link.objects.filter(Q(published=True),category=cate).order_by("-id")
        showAds=False
    # if(not showAds):
        # print("its 18+")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        if(not showAds):
            context["adsshow"]=True
        return render(request,"loadmore.html",context)
    seo = {
        'title': cate.name+" telegram groups and channels invite links "+str(date.today().year),
        "description": cate.name+" telegram group and channels: Are you searching for the best telegram channels for "+cate.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        "seo":seo
    }
    if(not showAds):
        context["adsshow"]=True
    return render(request,"index.html",context)

def country(request,path):
    cate=Country.objects.get(slug=path)
    postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot") & Q(country__slug=path)).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': cate.name+" telegram groups and channels invite links "+str(date.today().year),
        "description": cate.name+" telegram groups and channels: Are you searching for the best telegram channels for "+cate.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo
    }
    return render(request,"index.html",context)

def language(request,path):
    cate=Language.objects.get(slug=path)
    postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot")& Q(language__slug=path)).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': cate.name+" telegram groups and channels invite links "+str(date.today().year),
        "description": cate.name+" telegram groups and channels: Are you searching for the best telegram channels for "+cate.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo
    }
    return render(request,"index.html",context)

def tag(request,path):
    tag=Tag.objects.get(slug=path)
    postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot")& Q(tag__slug=path)).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': tag.name+" telegram groups and channels invite links "+str(date.today().year),
        "description": tag.name+" telegram groups and channels: Are you searching for the best telegram channels for "+tag.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo
    }

    return render(request,"index.html",context)

def search(request):
    # print(request.GET)
    keyword=request.GET['keyword']
    
    tag=Tag.objects.filter(Q(name__contains=keyword))
    coun = Country.objects.filter(Q(name__contains=keyword))
    cate = Category.objects.filter(Q(name__contains=keyword))
    lang = Language.objects.filter(Q(name__contains=keyword))
    postLink = Link.objects.filter(Q(name__contains=keyword) | Q(description__contains=keyword) | Q(
        tag__in=tag) | Q(country__in=coun) | Q(category__in=cate) | Q(language__in=lang)).order_by("-id")
    # postLink=list(set(postLink))
    postLink=postLink.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot"))
    
    postLink=list(set(postLink))
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
            "keyword": "keyword="+keyword
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': keyword+" telegram groups and channels invite links "+str(date.today().year),
        "description": keyword+" telegram groups and channels: Are you searching for the best telegram channels for "+keyword+" then check out this blog and join the group. Join Now",
        "robots": "noindex, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo,
        "keyword":"keyword="+keyword
    }
    return render(request,"index.html",context)

def addgroup(request):
    groupLink=request.POST['glink']
    categoryId=Category.objects.get(id=request.POST['category'])
    countryId=Country.objects.get(id=request.POST['country'])
    languageId=Language.objects.get(id=request.POST['language'])
    tags=request.POST['gtags']
    gtags=[]
    groupName, groupCount, groupLogo, groupDescri, groupType,linkId=tools.check(groupLink)
    groupCount=int(str(groupCount).replace(" ",""))
    # print(groupName, groupCount, groupLogo, groupDescri, groupType, linkId)
    if(groupLogo==0):
        message={
            "alertmsgbgcolor": '#f44336',
            "alertmsg":"This link is not acceptable!"
        }
        return groupfiles(request, "addgroup", message=message)
    if(len(Link.objects.filter(linkId=linkId))>0):
        message={
            "alertmsgbgcolor": '#f44336',
            "alertmsg":"This link already added"
        }
        return links(request, linkId,message=message)


    
    postLink=Link.objects.create(name=groupName,link=groupLink,category=categoryId,language=languageId,country=countryId,description=groupDescri,noOfMembers=groupCount,imgUrl=groupLogo,type=groupType,linkId=linkId)
    # Notification.objects.create(name="New group added",link=postLink)
    spTags = tags.split(",")
    try:
        spTags.remove("")
    except:pass
    for i in spTags:
        # print("tags:",i)
        try:
            tempTag=Tag.objects.create(name=i)
            gtags.append(tempTag)
        except:
            gtags.append(Tag.objects.get(name=i))
    for i in list(gtags):
        postLink.tag.add(i)
    context={
        "results":"result"
    }
    message = {
        "alertmsgbgcolor": '#04AA6D',
        "alertmsg": "Your link Successfully added"
    }
    return links(request, linkId, message=message)


def find(request):
    # print(request.GET)
    categoryId=request.GET.get('category')
    countryId=request.GET.get('country')
    languageId=request.GET.get('language')
    # print("Country id: ",categoryId)
    if(countryId == None):
        countryId = ""
    if categoryId == None:
        categoryId = ""
    if languageId == None:
        languageId = ""
    query="category="+categoryId+"&country="+countryId+"&language="+languageId
    result=""
    postLink={}
    filter_kwargs = {}

    is18plus=False
    if(categoryId!=""):
        cate=Category.objects.get(id=categoryId)
        filter_kwargs['category'] = cate
        result+=cate.name+", "
        if(cate.name=="Adult/18+/Hot"):
            is18plus=True


    if(countryId!=""):
        coun=Country.objects.get(id=countryId)
        filter_kwargs['country'] = coun
        result+=coun.name+", "

    if(languageId!=""):
        lang=Language.objects.get(id=languageId)
        filter_kwargs['language'] = lang
        result+=lang.name+", "

    postLink = Link.objects.filter(**filter_kwargs).order_by("-id")
    if(not is18plus):
        postLink=postLink.filter(~Q(category__name="Adult/18+/Hot"))
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        'keyword':query,
        }
        if(is18plus):
            context["adsshow"]=True
        return render(request,"loadmore.html",context)
    seo = {
        'title': result+" telegram groups and channels invite links "+str(date.today().year),
        "description": result+" telegram groups and channels: Are you searching for the best telegram channels for "+result+" then check out this blog and join the group. Join Now",
        "robots": "noindex, follow"
    }
    # print("Query: ",query)
    context={
        "links":pagination(request,postLink),
        "results":result,
        'seo':seo,
        'keyword':query,
    }

    if(is18plus):
        context["adsshow"]=True
    return render(request,"index.html",context)


def unlimited(request,path):

    postLink=Link.objects.filter(type=path.capitalize())
    seo = {
        'title': "unlimited telegram "+str(path)+" invite links "+str(date.today().year),
        "description":"unlimited telegram "+str(path)+" invite links "+str(date.today().year),
        "robots": "index, follow"
    }
    context={
        'links':postLink,
        'seo':seo
    }

    return render(request,'unlimited.html',context)

def randompost(request):
    random_link = random.choice(Link.objects.all())
    print('/join/'+random_link.linkId)
    return redirect('/join/'+random_link.linkId)

def unlimitedTelegramLinks(request):
    
    postLink=Link.objects.filter()
    # seo = {
    #     'title': str(len(postLink))+"+ Active Telegram Groups Links |Join, Submit|"+str(date.today().strftime("%d %b %Y")),
    #     "description":"Join 10,000+ Active popular Telegram groups Links in "+str(date.today().strftime("%Y"))+" | join and Share telegram groups and channels. Find most top category links on telekit",
    #     "robots": "index, follow"
    # }
    context={
        'links':postLink,
        # 'seo':seo
    }

    return render(request,'seoTest1.html',context)