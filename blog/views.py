# views.py
from ast import keyword
import datetime
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
from discordwebhook import Discord
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

year = '2024'

def send_email(subject, body, to_email):
    # Email configuration
    sender_email = "support@telekit.link"
    password = "1998Piriyaraj@"  # Use the email account’s password

    # SMTP server settings
    smtp_server = "telekit.link"
    smtp_port = 465

    # Create a MIMEText object for the email body
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Establish a secure connection with the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # Log in to the email account
            server.login(sender_email, password)

            # Send the email
            server.sendmail(sender_email, to_email, message.as_string())

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        

def pagination(request,obj):
    paginator = Paginator(obj, 6) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    linka = paginator.get_page(page_number)
    return linka

def links(request,path,message={}):
    try:
        postLink=Link.objects.filter(linkId=path)[0]
    except:
        return redirect("index")
    if(not postLink.published):
        return redirect("index")
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
        'title': str(date.today().year)+ " "+ postLink.name+" Telegram "+postLink.type+" link",
        "description": "Join active "+postLink.name+" Telegram "+postLink.type+" with ease. Discover what makes this "+postLink.type+" unique and engage with fellow members. Check out our blog for the latest invite link and start exploring today!",
        "robots": "index, follow",
        "ogimage": postLink.image_file.url,
        "tag":"Common"
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
    link=Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot")).order_by("-pointsperday","-modified")
    if(request.GET.get('page')):
        linka=pagination(request,link)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo={
        'title': f"9999+ Find Active telegram group & channel link List - {date.today().month}/{date.today().year}",
        "description": "Search & Join active telegram group links for Adults, movies, dating, education, and viral updates. Find unlimited telegram groups and channel links on Telekit.",
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
    try:
        cate=Category.objects.get(slug=path)
    except:
        return redirect("index")
    if(cate.name!="Adult/18+/Hot"):
        postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot"),category=cate).order_by("-modified")
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
        'title': f'9999+ {cate.name} Telegram Group & Channel links {year}',
        "description": f"Join 9999+ {cate.name} Telegram Group & Channel links. Are you searching for the {cate.name} Popular Telegram links then check out this blog and join the groups.",
        "robots": "index, follow",
        'tag': cate.name,
        'year': year,
    }
    context={
        "links":pagination(request,postLink),
        "seo":seo
    }
    if(not showAds):
        context["adsshow"]=True
    return render(request,"index.html",context)

def country(request,path):
    try:
        cate=Country.objects.get(slug=path)
    except:
        return redirect("index")
    postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot") & Q(country__slug=path)).order_by("-modified")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    # 1000+ Belgium Telegram Group Links & Channel List 2024
    # Join Belgium Telegram Group Links, Find a Guide about all tourist attractions in and around Belgium to visit and Check out. Learn Various languages like
    seo = {
        'title': f'9999+ {cate.name} Telegram Group & Channel links {year}',
        "description": f"Join 9999+ {cate.name} Telegram Group & Channel links. Are you searching for the {cate.name} Popular Telegram links then check out this blog and join the groups.",
        "robots": "index, follow",
        'tag': cate.name,
        'year': year,
        
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo,
        "country": cate.name,
    }
    return render(request,"index.html",context)

def language(request,path):
    try:
        cate=Language.objects.get(slug=path)
    except:
        return redirect("index")
    postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot")& Q(language__slug=path)).order_by("-modified")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': f'9999+ {cate.name} Telegram Group & Channel links {year}',
        "description": f"Join 9999+ {cate.name} Telegram Group & Channel links. Are you searching for the {cate.name} Popular Telegram links then check out this blog and join the groups.",
        "robots": "index, follow",
        'tag': cate.name,
        'year': year,
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo,
        "country": cate.name,
    }
    return render(request,"index.html",context)

def tag(request,path):
    try:
        tag=Tag.objects.get(slug=path)
    except:
        return redirect("index")
    postLink = Link.objects.filter(Q(published=True) & ~Q(category__name="Adult/18+/Hot")& Q(tag__slug=path)).order_by("-modified")
    if(request.GET.get('page')):
        linka=pagination(request,postLink)
        context={
        'links':linka,
        }
        return render(request,"loadmore.html",context)
    seo = {
        'title': f'9999+ {tag.name} Telegram Group & Channel links {year}',
        "description": f"Join 9999+ {tag.name} Telegram Group & Channel links. Are you searching for the {tag.name} Popular Telegram links then check out this blog and join the groups.",
        "robots": "index, follow",
        'tag': tag.name,
        'year': year,
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
        tag__in=tag) | Q(country__in=coun) | Q(category__in=cate) | Q(language__in=lang)).order_by("-modified")
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
        'title': keyword+" telegram groups and channels invite links "+year,
        "description": keyword+" telegram groups and channels: Are you searching for the best telegram channels for "+keyword+" then check out this blog and join the group. Join Now",
        "robots": "noindex, follow"
    }
    context={
        "links":pagination(request,postLink),
        'seo':seo,
        "keyword":"keyword="+keyword
    }
    return render(request,"index.html",context)

def DiscordNotification(Msg):
    webHookUrl = "https://discord.com/api/webhooks/1132597585824202813/8XDNjpwwOIsistL4nThyY7NjVo67UVHckbtOAAdGAf96_TZ7dTS3tOpDmle646rF_ZDX"
    discord = Discord(url = webHookUrl)
    discord.post(content=Msg)
    
def addgroup(request):
    if request.method == 'GET':
        return redirect('/group/addgroup')
    groupLink=request.POST['glink']
    categoryId=Category.objects.get(id=request.POST['category'])
    countryId=Country.objects.get(id=request.POST['country'])
    languageId=Language.objects.get(id=request.POST['language'])
    to_mail = request.POST['mail']
    tags=request.POST['gtags']
    gtags=[]
    print(f"======> Adding: {groupLink}")
    groupName, groupCount, groupLogo, groupDescri, groupType,linkId=tools.check(groupLink)
    groupCount=int(str(groupCount).replace(" ",""))
    # print(groupName, groupCount, groupLogo, groupDescri, groupType, linkId)
    if(groupLogo==0):
        message={
            "alertmsgbgcolor": '#f44336',
            "message":"This link is not acceptable!"
        }
        # print("   [-] This link is not acceptable!")
        return render(request,"groupaddresult.html",message)
    link_objs_to_delete = Link.objects.filter(linkId__contains=linkId + "_*_")

    # Check if the object(s) exist before deleting
    if link_objs_to_delete.exists():
        # Delete the Link object(s)
        link_objs_to_delete[0].delete()
    linkObj = Link.objects.filter(Q(linkId=linkId) | Q(imgUrl=groupLogo))
    
    if(len(linkObj)>0):
        # print(linkObj[0].modified)
        # '2024-04-28 04:33:48.641650+00:00' 
        # modified_time = datetime.datetime.strptime(str(linkObj[0].modified), '%Y-%m-%d %H:%M:%S.%f%z')

        # Get the current time
        current_time = datetime.datetime.now()
        modified_time_naive = linkObj[0].modified.replace(tzinfo=None)
        # Calculate the time difference
        time_difference = current_time - modified_time_naive

        # Extract the hours from the time difference
        hours_since_update = time_difference.total_seconds() / 3600
        # print(hours_since_update)
        if(hours_since_update>=24):
            linkObj[0].noOfMembers = groupCount
            linkObj[0].save()
            message={
                "alertmsgbgcolor": '#04AA6D',
                "message":"Great your link placed in first place.",
            }
        else:
            message={
                "alertmsgbgcolor": '#f44336',
                "message":"oops! submit your link after "+str(24-int(hours_since_update))+" Hours",
            }
        context={
            'links':linkObj,
        }
        context.update(message)
        # print(f"   [-] {message['message']}")
        return render(request,"groupaddresult.html",context)

    code_length = 10
    unique_code = secrets.token_hex(code_length // 2)
        
    postLink=Link.objects.create(name=groupName,link=groupLink,category=categoryId,language=languageId,country=countryId,description=groupDescri,noOfMembers=groupCount,imgUrl=groupLogo,type=groupType,linkId=linkId+"_*_"+unique_code,published = False,mail = to_mail)
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
        
    linkObj =Link.objects.filter(linkId=linkId+"_*_"+unique_code)
    if linkObj.exists():
        link_obj = linkObj.first()

        # Create a copy of the object to work with
        temporary_link_obj = link_obj.__class__.objects.get(pk=link_obj.pk)

        # Modify the attribute temporarily
        temporary_link_obj.linkId = linkId
    context={
            'links':[temporary_link_obj],
    }
    message = {
        "alertmsgbgcolor": '#90a316',
        "message": "Status: Pending, Check your mail and verify your mail address"
    }
    # print(f"   [-] {message['message']}")
    current_domain = request.get_host()
    verification_link = f"https://{current_domain}/verify?code={linkId+'_*_'+unique_code}"
    subject = "Mail verification - Telekit.link"
    body = f"""
    Welcome to Telekit.link
    
    Your Telegram group/Channel has been Added successfully.
    
    click the below link to verify your email address
    
    {verification_link}
    
    Thank you
    Regards
    Telekit.link
    """
    send_email(subject,body,to_mail)
    context.update(message)

    return render(request,"groupaddresult.html",context)
    return links(request, linkId, message=message)

def verify(request):
    # Retrieve the verification code from the GET parameters
    verification_code = request.GET.get('code', '')
    # print("================>", verification_code)
    if verification_code[0]== ' ':
        verification_code = '+'+verification_code.strip()
    # Check if the verification code is empty and redirect to 'index' if so
    if verification_code == '':
        # print("================> Verification code not found")
        return redirect("index")

    # Split the verification_code to extract linkId
   
    # print("================>",verification_code)
    # Query the Link model to get the Link object based on the extracted linkId
    linkObj = Link.objects.filter(linkId=verification_code)
    # print("================>", str(len(linkObj)))
    # Check if the Link object exists
    if not linkObj.exists():
        # print("================> link not exit")
        
        # Handle the case where the Link object does not exist (you may want to redirect or show an error message)
        return redirect("index")  # Adjust the redirect target as needed
    
    linkId = verification_code.split("_*_")[0]
    # print("================>", linkId)
    # Update the Link object attributes and save it
    linkObj = linkObj[0]  # Assuming you are confident that the linkObj exists, otherwise handle accordingly
    linkObj.linkId = linkId
    linkObj.published = True
    linkObj.save()

    # Prepare the context for rendering the template
    context = {
        'links': [linkObj],  # Place the Link object in a list if needed for consistency
        'alertmsgbgcolor': '#04AA6D',
        'message': "Status: Accepted, Congratulations, your email is verified, and your link is successfully added."
    }
    print("============>",linkObj.category.name)
    try:
        if linkObj.category.name != "Adult/18+/Hot":
            DiscordNotification(f"TELEKIT: Added new link https://telekit.link/join/{linkId}")
    except Exception as e:
        DiscordNotification(f"TELEKIT: Error {e}")
    # Render the template with the updated context
    return render(request, "groupaddresult.html", context)

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
    postLink=postLink.filter(Q(published=True))
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
        'title': result+" telegram groups and channels invite links "+year,
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
        'title': "unlimited telegram "+str(path)+" invite links "+year,
        "description":"unlimited telegram "+str(path)+" invite links "+year,
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

@user_passes_test(lambda u: u.is_superuser)
def changeCategory(request,path):
    try:
        link = Link.objects.get(linkId=path)
        newCategory = Category.objects.get(name="Adult/18+/Hot")

        link.category = newCategory
        link.save()
        return JsonResponse({'message': 'Category changed successfully'})
    except Link.DoesNotExist:
        return JsonResponse({'message': 'Link not found'})
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found'})


def landing_view(request):
    link_param = request.GET.get('link', '')  # Get the value of the 'link' parameter
    if link_param == '':
        return redirect("index") 
    seo = {
        'title': f'Landing page for join group/channel',
        "description": f"Joining the group/channel",
        "robots": "noindex, nofollow",
    }
    context={
        'seo':seo,
        'link_param': link_param
    }

    return render(request, 'landing.html', context)


def mail_test(request):
    # Your email details
    subject = 'Hello, Django!'
    message = 'This is a test email sent from a Django web application.'
    from_email = 'support@telekit.link'
    recipient_list = ['piriyaraj1998@gmail.com']  # Replace with the recipient's email address

    # Use the send_mail function
    try:
        send_email(subject, message, recipient_list[0])

        # You can customize the response or redirect to another page
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Email sent Failed!: {e}')
