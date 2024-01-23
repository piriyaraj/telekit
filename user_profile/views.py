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

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        
        
from .models import Linkpin, User
# from notification.models import Notificaiton


@never_cache
@not_logged_in_required
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            print(user.verified)
            if user:
                if not user.verified:
                    messages.warning(request, "Verification Required: Confirm Your Email Address")
                    return redirect('login')
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, "Wrong credentials")
    seo = {
        "robots": "noindex, nofollow"
    }
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

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        print("Form errors:", form.errors)
        print("Is form valid?", form.is_valid())
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
            return redirect('login')
    seo = {
        "robots": "noindex, nofollow"
    }
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
    print(links)
    context={
      'links':links,
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
    points_list = Link.objects.filter(pointsperday__gt=0).order_by('-pointsperday').values_list('pointsperday', flat=True)
           # from datetime import timedelta
    total_points = request.user.points
    
    allocated = 1
    if pin_link_obj:
        pin_link_obj = pin_link_obj[0]
    # Assuming pin_link_obj is a LinkPin instance
        timenow = timezone.now()

        # Calculate the duration since the link was pinned
        duration = timenow - pin_link_obj.added
        # Calculate the available points based on the duration and points_per_day
        days = duration.total_seconds()/86400
        allocated = pin_link_obj.points - (pin_link_obj.points_per_day * days)

        # If available points are negative, set them to zero
        total_points = total_points + max(allocated, 0)
        
    if request.method == 'POST':
        form = Pinlinks(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days']
            points = form.cleaned_data['points']

            # Calculate points per day
            points_per_day = int(points) / int(days)

            # Create a new LinkPin record
            if pin_link_obj:
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

            # Update user points and link points per day
            # 1997 - 997
            lessPoint = points - allocated +1
            request.user.points = request.user.points - lessPoint
            request.user.save()
            link_obj.pointsperday = points_per_day
            link_obj.save()

            return redirect('profile')  # Redirect to a success page or another URL after pinning

    else:

        form = Pinlinks(max_points=total_points,min_points= allocated)

    context = {
        'links': [link_obj],
        'form': form,  
        'points': list(points_list)
     }


    return render(request, "user_profile/pin.html", context)


def mail_verify(request,path):
    mail,verification_code = path.split('_*_')
    try:
        userObj = User.objects.get(email=mail,verification_id=verification_code)
        userObj.verified = True
        userObj.save()
        messages.success(request, "Your account has been verified login now!")
        print("=================Your account has been verified login now!")
    except User.DoesNotExist:
        print("=================Try again: Failed to verify your account")
    return redirect('login')