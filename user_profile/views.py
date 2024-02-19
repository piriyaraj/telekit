from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from blog.models import Link
import uuid
from .forms import (
    UserRegistrationForm,
    LoginForm,
    Pinlinks
)
from .decorators import  (
    not_logged_in_required
)

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

        # print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # pass
        
        
from .models import Linkpin, User
# from notification.models import Notificaiton


@never_cache
@not_logged_in_required
def login_user(request):
    form = LoginForm()
    seo = {
        'title': f'Log into Telekit.link.',
        "description": f"Securely log into Telekit.link for seamless access to your account. Experience hassle-free authentication and enjoy the features of Telekit with confidence. Your gateway to a personalized and secure online experience.",
        "robots": "index, follow",
    }
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            # print(user.verified)
            if user:
                if not user.verified:
                    # messages.warning(request, "Verification Required: Confirm Your Email Address")
                    # form['verification'] = "Verification Required: Confirm Your Email Address"
                    return render(request, 'user_profile/login.html', {'message': "Verification Required: Confirm Your Email Address"})
                login(request, user)
                return redirect('index')
            else:
                # messages.warning(request, "Wrong credentials")
                return render(request, 'user_profile/login.html', {'message': "Wrong credentials","seo":seo})
    context = {
        "form": form,
        "seo":seo
    }
    return render(request, 'user_profile/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')

def verification_id_gen():
    return str(uuid.uuid4())

@never_cache
@not_logged_in_required
def register_user(request):
    seo = {
        'title': f'Sign Up for Telekit.link',
        'description': 'Create a new account on Telekit.link for access to exclusive features. Join now and enjoy a personalized and secure online experience.',
        'robots': 'index, follow',
    }
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        # print("Form errors:", form.errors)
        # print("Is form valid?", form.is_valid())
        if form.is_valid():
            current_domain = request.get_host()
            mail = form.cleaned_data.get('email')
            verification_id = verification_id_gen()
            verification_link = f"https://{current_domain}/mailverify/{mail+'_*_'+verification_id}"
            subject = "Mail verification - Telekit.link"
            body = f"""
            Welcome to Telekit.link
            
            click the below link to verify your email address
            
            {verification_link}
            
            Thank you
            Regards
            Telekit.link
            """

            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.verification_id = verification_id
            user.save()
            send_email(subject,body,mail)
            messages.success(request, "Check your inbox: Confirm your email address")
            seo = {
                'title': f'Log into Telekit.link.',
                "description": f"Securely log into Telekit.link for seamless access to your account. Experience hassle-free authentication and enjoy the features of Telekit with confidence. Your gateway to a personalized and secure online experience.",
                "robots": "noindex, nofollow",
            }
            return render(request, 'user_profile/login.html', {'message': "Verification Required: Check you inbox @ Confirm Your Email Address","seo":seo})
        else:
            return render(request, 'user_profile/registration.html', {'form': form,"seo":seo})

    form = UserRegistrationForm()
    context = {
        "form": form,
        'seo':seo
    }
    return render(request, 'user_profile/registration.html', context)


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    links = account.links.all()
    seo = {
    'title': f'{account.username} Profile on Telekit.link',
    'description': 'Explore and manage your Telekit.link profile. View and update your information, preferences, and settings. Your personalized hub for a seamless online experience.',
    'robots': 'noindex, nofollow',
    }
    context={
      'links':links,
      "seo":seo
    }
    return render(request, 'user_profile/profile.html',context)

@login_required
def addlinkprofile(request, path):
    # Assuming 'path' corresponds to the linkId in your Link model
    link = get_object_or_404(Link, linkId=path)
    
    user = request.user
    user.links.add(link)
    user.save()
    # Optionally, you can return a JsonResponse indicating success
    return JsonResponse({'message': 'Link added successfully'})

@login_required
def removelinkprofile(request, path):
    # Assuming 'path' corresponds to the linkId in your Link model
    link = get_object_or_404(Link, linkId=path)
    
    user = request.user
    user.links.remove(link)
    user.save()
    # Optionally, you can return a JsonResponse indicating success
    return JsonResponse({'message': 'Link removed successfully'})


def view_user_information(request, username):
    account = get_object_or_404(User, username=username)
    following = False
    muted = None

    if request.user.is_authenticated:
        
        if request.user.id == account.id:
            return redirect("profile")

        followers = account.followers.filter(
        followed_by__id=request.user.id
        )
        if followers.exists():
            following = True
    
    if following:
        queryset = followers.first()
        if queryset.muted:
            muted = True
        else:
            muted = False
    seo = {
        "robots": "noindex, nofollow"
    }
    context = {
        "account": account,
        "following": following,
        "muted": muted,
        'seo':seo
    }

    return render(request, "user_information.html", context)


@login_required(login_url="login")
def pinLink(request, path):
    link_obj = Link.objects.get(linkId=path)
    pin_link_obj = Linkpin.objects.filter(linkId=path)
    seo = {
        'title': f'Pin {link_obj.name} on Telekit.link',
        'description': f'Pin {link_obj.name} on Telekit.link to get more members to your {link_obj.type}',
        'robots': 'index, follow',
    }
    if link_obj.category.name != "Adult/18+/Hot":
        points_list = Link.objects.filter(Q(pointsperday__gt=0) & ~Q(category__name="Adult/18+/Hot")).order_by('-pointsperday').values_list('pointsperday', flat=True)
           # from datetime import timedelta
    else:
        points_list = Link.objects.filter(Q(pointsperday__gt=0) & Q(category__name="Adult/18+/Hot")).order_by('-pointsperday').values_list('pointsperday', flat=True)
    total_points = request.user.points
    available_points = 0
    context = {
        'links': [link_obj],
        'points': list(points_list),
        "seo":seo,
        "old_points":available_points,
    }

    if pin_link_obj:
        timenow = timezone.now()

        # Calculate the duration since the link was pinned
        duration = pin_link_obj[0].modified - timenow
        # print("added:",pin_link_obj[0].modified)
        # print("Now:",timenow)
        duration = duration.total_seconds() + pin_link_obj[0].days*(60*60*24)
        if duration>0:
            duration = duration/(60*60*24)
            # print("days: ", duration)
            # print("points: ", duration*pin_link_obj[0].points_per_day)
            available_points = int(duration*pin_link_obj[0].points_per_day)
            context['old_points'] = available_points

    if request.method == 'POST':
        form = Pinlinks(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days']
            points = form.cleaned_data['points']
            required_points = int(points)

            # Create a new LinkPin record
            



            if request.user.points < int(required_points):
                context['message'] = "Please enter the valid point"
                context['form'] = Pinlinks(max_points=total_points,min_points= 1)
                return render(request, "user_profile/pin.html", context)
            points = int(points)+available_points
            # Calculate points per day
            points_per_day = int(points) / int(days)
            # print("New Points:",points)
            if pin_link_obj:
                pin_link_obj = pin_link_obj[0]
                pin_link_obj.days = int(days)
                pin_link_obj.points = points
                pin_link_obj.points_per_day = points_per_day
                pin_link_obj.save()
            else:
                link_pin = Linkpin.objects.create(
                    points=points,
                    days=int(days),
                    points_per_day=points_per_day,
                    user=request.user,
                    linkId=path
                )
            request.user.points = request.user.points - int(required_points)
            request.user.save()
            link_obj.pointsperday = points_per_day
            link_obj.save()

            return redirect('profile')  # Redirect to a success page or another URL after pinning

    else:
        context['form'] = Pinlinks(max_points=total_points, min_points=1)

    return render(request, "user_profile/pin.html", context)


def mail_verify(request,path):
    mail,verification_code = path.split('_*_')
    try:
        userObj = User.objects.get(email=mail,verification_id=verification_code)
        userObj.verified = True
        userObj.save()
        messages.success(request, "Your account has been verified login now!")
        # print("=================Your account has been verified login now!")
    except User.DoesNotExist:
        print("=================Try again: Failed to verify your account")
    return render(request, 'user_profile/login.html', {'message': "Successfully verified your account! log in now!"})