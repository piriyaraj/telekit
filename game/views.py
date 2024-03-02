from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Spin, ReferralCount, ReferralVisit
from django.utils import timezone
from django.shortcuts import redirect, render
from user_profile.models import User
@login_required(login_url='login')
def spinner(request):
    user = request.user
    seo = {
        'title': f'Spin and earn free points and pin your link on telekit.link',
        'description': 'Get free points and pin your link on telekit',
        'robots': 'noindex, nofollow',
    }
    try:
        # Retrieve the user's spin record, or create a new one if it doesn't exist
        spin = Spin.objects.get(user=user)
    except Spin.DoesNotExist:
        spin = Spin(user=user)
        spin.save()

    wait_time = spin.can_spin_now()
    spin_count = spin.get_spin_count_today()
    if wait_time>=3600:
        # print("User can spin now")
        # User can spin now, perform the spin logic
        # Note: Add your spinning logic here, and update the last_spin field accordingly
        # For example, you might update the last_spin field after a successful spin
        # spin.last_spin = timezone.now()
        # spin.save()
        return render(request, 'game/spin.html',{"spin":True,'wait_time':0,'spin_count':spin_count})
        # Notify the user if more than 1 day has passed since the last spin
        spin.notify_user()

        # Add your logic to determine the selected value after the spin
        selected_value = 25  # Replace this with your actual logic

        # Render the template with the selected value
        
    else:
        # User needs to wait before spinning again
        # return render(request, 'game/spin.html',{"spin":False,'wait_time':36})
        return render(request, 'game/spin.html',{"spin":False,'wait_time':3600-wait_time,"seo":seo,'spin_count':spin_count})

@login_required(login_url='login')
def spinHandler(request,points):
    user = request.user
    spin = Spin.objects.get(user=user)

    if spin.can_spin_now()>=3600 and int(points)<=50:
        user.points += int(points)
        user.save()
        current_time = timezone.now()
        
        if spin.last_spin and spin.last_spin.date() == current_time.date():
            # If yes, increment today_spin_count
            spin.today_spin_count += 1
        else:
            # If no, set today_spin_count to 1
            spin.today_spin_count = 1
        spin.last_spin = timezone.now()
        spin.save()
        return JsonResponse({'message': 'Your score updated successfully'})
    else:
        return redirect('spin-earn-points')
    
    
@login_required(login_url='login')
def claim_bonus(request):
    user = request.user
    spin = Spin.objects.get(user=user)

    if spin.today_spin_count >= 10:
        user.points += 100
        user.save()
        spin.today_spin_count -= 10
        spin.save()
        return JsonResponse({'status': True, 'message': 'Congratulations! You got 100 points'})
    else:
        return JsonResponse({'status': False, 'message': 'You need to complete 10 spins within one day.'})

@login_required(login_url='login')
def referral(request):
    seo = {
        'title': f'Earn points by sharing your referral',
        'description': 'Get free points and pin your link on telekit',
        'robots': 'noindex, nofollow',
    }
    context ={
        "referral_count": ReferralCount.objects.all().order_by("-count"),
        "seo": seo,
    }
    return render(request,'game/referral.html',context)

def referral_handler(request,referral_code):
    referral_code = int(referral_code.replace("telekit",''))
    user = User.objects.get(id=referral_code)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    is_exist = ReferralVisit.objects.filter(user=user,ip = ip)
    
    if is_exist:
        return redirect('index')
    
    ReferralVisit.objects.create(user=user,ip=ip)
    
    referral = ReferralCount.objects.filter(user=user)
    
    if referral:
        referral = referral[0]
        referral.count += 1
        referral.save()
        return redirect('index')
    
    ReferralCount.objects.create(user=user,count = 1)
    return redirect('index')