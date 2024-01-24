from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Spin
from django.utils import timezone
from django.shortcuts import redirect, render
@login_required(login_url='login')
def spinner(request):
    user = request.user
    try:
        # Retrieve the user's spin record, or create a new one if it doesn't exist
        spin = Spin.objects.get(user=user)
    except Spin.DoesNotExist:
        spin = Spin(user=user)
        spin.save()

    wait_time = spin.can_spin_now()
    print(wait_time)
    if wait_time>=3600:
        print("User can spin now")
        # User can spin now, perform the spin logic
        # Note: Add your spinning logic here, and update the last_spin field accordingly
        # For example, you might update the last_spin field after a successful spin
        # spin.last_spin = timezone.now()
        # spin.save()
        return render(request, 'game/spin.html',{"spin":True})
        # Notify the user if more than 1 day has passed since the last spin
        spin.notify_user()

        # Add your logic to determine the selected value after the spin
        selected_value = 25  # Replace this with your actual logic

        # Render the template with the selected value
        
    else:
        # User needs to wait before spinning again
        # return render(request, 'game/spin.html',{"spin":False,'wait_time':36})
        return render(request, 'game/spin.html',{"spin":False,'wait_time':3600-wait_time})

@login_required(login_url='login')
def spinHandler(request,points):
    user = request.user
    spin = Spin.objects.get(user=user)

    if spin.can_spin_now()>=3600 and int(points)<=50:
        user.points += int(points)
        user.save()
        spin.last_spin = timezone.now()
        spin.save()
        return JsonResponse({'message': 'Your score updated successfully'})
    else:
        return redirect('spin-earn-points')