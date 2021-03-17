from django.shortcuts import render
from led_colors.models import Client, ColorProfile
from django.http import JsonResponse,HttpResponseRedirect
# Create your views here.
def realtime(request, key):
    user = request.user
    if user.is_authenticated:
        clients = Client.manager.clients_for_user_id(user.id)
        master_color,_ = ColorProfile.objects.get_or_create(name="master_"+str(user.id))
        Client.manager.set_realtime(user.id,True)
        return render(request, 'realtimemaster.html',{'current_color':master_color,'key': key})
    return HttpResponseRedirect(reverse("login")) 