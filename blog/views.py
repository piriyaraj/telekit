from ast import keyword
from multiprocessing import context
from os import link
from re import L
import re
from unicodedata import category
from unittest import result
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from blog.models import Category, Company, Country, Language, Link, Tag
from . import tools
from django.core.paginator import Paginator

def pagination(request,obj):
    paginator = Paginator(obj, 6) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    linka = paginator.get_page(page_number)
    return linka

def links(request,path):
    postLink=Link.objects.filter(linkId=path)[0]
    country=postLink.country
    language=postLink.language
    category=postLink.category
    relatedLink=Link.objects.filter(country=country,language=language,category=category)
    
    context={
        "post":postLink,
        "links":relatedLink
    }
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
        'title':"Telekit - Enjoy Unlimited Telegram Group and channel Links Invite to Join",
        "description":"Enjoy Unlimited Telegram groups and channel invite link to join Telegram gorup and channel. Here you can find verious type of Telegram join links.",
        "robots":"index, follow"
    }
    linka=pagination(request,link)
    context={
      'links':linka,
      'seo':seo
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

def groupfiles(request,path):

    file="group/"+path+".html"
    return render(request,file)


def category(request,path):
    cate=Category.objects.get(slug=path)
    postLink=Link.objects.filter(category=cate)
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo={
        'title':"Telekit - Enjoy Unlimited Telegram Group and channel Links Invite to Join",
        "description":"Enjoy Unlimited Telegram groups and channel invite link to join Telegram gorup and channel. Here you can find verious type of Telegram join links.",
        "robots":"index, follow"
    }
    context={
        "links":pagination(request,postLink),
        "seo":seo
    }
    return render(request,"index.html",context)

def country(request,path):
    cate=Country.objects.get(slug=path)
    postLink=Link.objects.filter(country=cate) 
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    context={
        "links":pagination(request,postLink)
    }
    return render(request,"index.html",context)

def language(request,path):
    cate=Language.objects.get(slug=path)
    postLink=Link.objects.filter(language=cate) 
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    context={
        "links":pagination(request,postLink)
    }
    return render(request,"index.html",context)

def tag(request,path):
    tag=Tag.objects.get(slug=path)
    postLink=Link.objects.filter(tag=tag) 
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    context={
        "links":pagination(request,postLink)
    }
    return render(request,"index.html",context)

def search(request):
    keyword=request.GET['keyword']
    tag=Tag.objects.filter(Q(name__contains=keyword))
    postLink=Link.objects.filter(Q(name__contains=keyword)|Q(description__contains=keyword)|Q(tag__in=tag))
    # postLink+=Link.objects.filter(description__contains=keyword)
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    context={
        "links":pagination(request,postLink)
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
    # print(groupName, groupCount, groupLogo, groupDescri, groupType)

    if(len(Link.objects.filter(linkId=linkId))>0):
        return redirect("/join/"+linkId)

    
    postLink=Link.objects.create(name=groupName,link=groupLink,category=categoryId,language=languageId,country=countryId,description=groupDescri,noOfMembers=groupCount,imgUrl=groupLogo,type=groupType,linkId=linkId)
    for i in tags.split(","):
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
    return redirect("/join/"+linkId,context)


def find(request):
    categoryId=request.GET.get('category')
    countryId=request.GET.get('country')
    languageId=request.GET.get('language')
    print((categoryId,categoryId,languageId))
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

    postLink=Link.objects.filter(**filter_kwargs)
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)

    context={
        "links":pagination(request,postLink),
        "results":result
    }
    return render(request,"index.html",context)