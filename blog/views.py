from ast import keyword
from email import message
from multiprocessing import context
from os import link
from re import L
import re
from unicodedata import category
from unittest import result
from wsgiref.util import request_uri
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from blog.models import Category, Company, Country, Language, Link, Tag
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
    relatedLink = Link.objects.filter(country=country, language=language, category=category).order_by("-id")
    relatedLink=relatedLink.exclude(id=postLink.id)
    if(request.GET.get('page')):
        linka = pagination(request, relatedLink)
        context = {
            'links': linka,
        }
        return render(request, "loadmore.html", context)

    linka = pagination(request, relatedLink)
    seo = {
        'title': postLink.name+" telegram "+postLink.type+" invite link "+str(date.today().year),
        "description": postLink.name+" telegram "+postLink.type+" invite link Are you searching for active "+postLink.name+" telegram invite link then check out this blog and join the "+postLink.type,
        "robots": "index, follow",
        "ogimage": postLink.image_file.url
    }
    context={
        "post":postLink,
        "links": linka,
        'seo':seo
    }
    context.update(message)
    return render(request,"links.html",context)

def index(request):
    link=Link.objects.order_by("-id")

    if(request.GET.get('page')):
        linka=pagination(request,link)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo={
        'title': "Telekit - Unlimited Telegram Group and channel invite links",
        "description": "Enjoy Unlimited Telegram groups and channel invites links to join Telegram group and channel. Here you can find various types of Telegram join links.",
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
    return render(request,file)


def groupfiles(request, path, message={}):

    file="group/"+path+".html"
    return render(request, file, message)


def category(request,path):
    cate=Category.objects.get(slug=path)
    postLink = Link.objects.filter(category=cate).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': cate.name+" category telegram groups and channels invite links "+str(date.today().year),
        "description": cate.name+" category telegram group and channels: Are you searching for the best telegram channels for "+cate.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        "seo":seo
    }
    return render(request,"index.html",context)

def country(request,path):
    cate=Country.objects.get(slug=path)
    postLink = Link.objects.filter(country=cate).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': cate.name+" country telegram groups and channels invite links "+str(date.today().year),
        "description": cate.name+" country telegram groups and channels: Are you searching for the best telegram channels for "+cate.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo
    }
    return render(request,"index.html",context)

def language(request,path):
    cate=Language.objects.get(slug=path)
    postLink = Link.objects.filter(language=cate).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': cate.name+" language telegram groups and channels invite links "+str(date.today().year),
        "description": cate.name+" language telegram groups and channels: Are you searching for the best telegram channels for "+cate.name+" then check out this blog and join the group. Join Now",
        "robots": "index, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo
    }
    return render(request,"index.html",context)

def tag(request,path):
    tag=Tag.objects.get(slug=path)
    postLink = Link.objects.filter(tag=tag).order_by("-id")
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
    keyword=request.GET['keyword']
    tag=Tag.objects.filter(Q(name__contains=keyword))
    coun = Country.objects.filter(Q(name__contains=keyword))
    cate = Category.objects.filter(Q(name__contains=keyword))
    lang = Language.objects.filter(Q(name__contains=keyword))
    postLink = Link.objects.filter(Q(name__contains=keyword) | Q(description__contains=keyword) | Q(
        tag__in=tag) | Q(country__in=coun) | Q(category__in=cate) | Q(language__in=lang)).order_by("-id")
    # postLink=list(set(postLink))
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
            "keyword": keyword
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
        "keyword":keyword
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
    spTags = tags.split(",")
    spTags.remove("")
    for i in spTags:
        print("tags:",i)
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
    categoryId=request.GET.get('category')
    countryId=request.GET.get('country')
    languageId=request.GET.get('language')
    result=""
    postLink={}
    filter_kwargs = {}


    if(categoryId!=""):
        cate=Category.objects.get(id=categoryId)
        filter_kwargs['category'] = cate
        result+=cate.name+", "


    if(countryId!=""):
        coun=Country.objects.get(id=countryId)
        filter_kwargs['country'] = coun
        result+=coun.name+", "

    if(languageId!=""):
        lang=Language.objects.get(id=languageId)
        filter_kwargs['language'] = lang
        result+=lang.name+", "

    postLink = Link.objects.filter(**filter_kwargs).order_by("-id")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': result+" telegram groups and channels invite links "+str(date.today().year),
        "description": result+" telegram groups and channels: Are you searching for the best telegram channels for "+result+" then check out this blog and join the group. Join Now",
        "robots": "noindex, follow"
    }
    context={
        "links":pagination(request,postLink),
        "results":result,
        'seo':seo
    }
    return render(request,"index.html",context)