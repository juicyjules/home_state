from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Client, ColorProfile
from .forms import ClientForm, ColorProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import re
# Create your views here.
def main(req):
    user = req.user
    if user.is_authenticated:
        return  HttpResponseRedirect(reverse("master"))
    else:
        return HttpResponseRedirect(reverse("login"))
    
def master(req):
    user = req.user
    if user.is_authenticated:
        clients = Client.manager.clients_for_user_id(user.id)
        master_color,_ = ColorProfile.objects.get_or_create(name="master_"+str(user.id))
        if req.method == "POST":
            color = req.POST.get("color","")
            on = req.POST.get("on",None)
            if color:
                try:
                    data = color.strip().replace("#","")
                    if len(data)>8:
                        raise Exception("Too big anyways")
                    iColor = int(data,16)
                    color = data.lower()
                    clean_color = color
                except:
                    clean_color = master_color.color
            else:
                clean_color = master_color.color
            if on != None:
                clean_on = on
                Client.manager.turn_on(user.id,clean_on) 
            master_color.color = clean_color
            master_color.save() 
            Client.manager.set_master_color(user.id,master_color.id)
            return JsonResponse({"message":"success"})
        else:
            all_on = all(map(lambda c: c.on,clients))
            print(all_on)
            return render(req,"master.html",{ "name": master_color.name,"color": master_color.color, "url":req.get_full_path(),"all_on": all_on})
    else:
        return HttpResponseRedirect(reverse("login"))
def clients(req):
    user = req.user
    if user.is_authenticated:
        clients = Client.manager.clients_for_user_id(user.id)
        return render(req, "clients.html", {'clients' : list(clients)})
    else:
        return HttpResponseRedirect(reverse("login"))
def colors(req):
    user = req.user
    if user.is_authenticated:
        profiles = ColorProfile.objects.all()
        print(profiles)
        return render(req, "colors.html", {'profiles' : list(profiles)})
    else:
        return HttpResponseRedirect(reverse("login"))

def create_client(req):
    user = req.user
    if user.is_authenticated:
        if req.method == 'POST':
            form = ClientForm(req.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                color = form.cleaned_data['profile_choice']
                client = Client(name=name,owner_id=user.id,current_profile=color)
                client.save()
                return HttpResponseRedirect(reverse("clients"))
            else:
                return HttpResponse("Ne das läuft nid")
        else:
            form = ClientForm()
            return render(req, "create_client.html", {'form' : form, "url" : reverse("create_client")})
    else:
        return HttpResponseRedirect(reverse("login"))
def client_info(req,key):
    is_uuid = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if is_uuid.match(key):
        client = Client.manager.get_client_for_key(key)
        data = {
            'key' : client.key,
            'name' : client.name,
            'color' : client.current_profile.color if client.current_profile else None ,
            'owner' : str(client.owner),
            'last_connection' : client.last_connection,
            'on' : client.on
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Client does not exist")

@csrf_exempt
def client_toggle(req,key):
    is_uuid = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if is_uuid.match(key):
        client = Client.manager.get_client_for_key(key)
        client.on = not client.on
        client.save()
        data = {
            'on' : client.on,
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Client does not exist")

@csrf_exempt
def master_toggle(req,key):
    if req.method == "POST":
        is_uuid = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        if key == "4ac25e64-6985-46dd-9878-0bae91c48519":
            try:
                data = json.loads( req.body.decode('utf-8'))
            except:
                return HttpResponse("Wrong JSON")
            on = data["on"]
            if on != None and type(on) == bool:
                clean_on = on
                Client.manager.turn_on(1,clean_on) 
                data = {
                    "on": clean_on
                }
            else:
                data = {
                    "on": False
                }
            return JsonResponse(data)
        else:
            return HttpResponseNotFound("wrong Masterkey")
    return HttpResponseNotFound("no Post")

def client_edit(req,key):
    is_uuid = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    if is_uuid.match(key):
        client = Client.manager.get_client_for_key(key)
        if req.method == 'POST':
            form = ClientForm(req.POST,instance=client)
            if form.is_valid():
                edit = form.save(commit=False)
                # TODO RAUSFINDEN WIESO ES WENN ES COMMIT KEINE  FEHLER SCHMEIßT ABER STROTZDEM nicht speicher
                # Ich habe legit keine Ahnung, finde auch sonst nichts. Sonst hat es gemeckert von wegen Datentyp
                # Aber jetzt ist alles Kacke und ich will nid mehr geh gleich Heim ey
                # Also echt kein Plan Warum das Form A) Etwas falsches Saven will, B) Nicht Saved ohne fehler mit der save() function
                # Und C ja keine ahung ey
                # Habs rausgefunde: ITS NOT FUCKING LINKED IN THE FUCKING FORM FUCK
                edit.current_profile_id = form.cleaned_data["profile_choice"].id
                edit.save(update_fields=["current_profile","name"])
                return HttpResponseRedirect(reverse("clients"))
            else:
                return HttpResponse("Ne das läuft nid")
        else:
            form = ClientForm(instance=client,initial={"profile_choice":client.current_profile})
            print(req.GET)
            return render(req, "create_client.html", {'form' : form, "url" : req.get_full_path()})
    else:
        return HttpResponseNotFound("Client does not exist")

def edit_color(req,name):
    user = req.user
    if user.is_authenticated:
        color = get_object_or_404(ColorProfile,name=name)
        if req.method == 'POST':
            form = ColorProfileForm(req.POST,instance=color)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("colors"))
            else:
                return HttpResponse("Ne das läuft nid")
        else:
            form = ColorProfileForm(instance=color)
            return render(req, "create_color.html", {'form' : form, "head": "Edit Color","url" : req.get_full_path()})
    else:
        return HttpResponseNotFound("Client does not exist")

def create_color(req):
    user = req.user
    if user.is_authenticated:
        if req.method == 'POST':
            form = ColorProfileForm(req.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                color = form.cleaned_data["color"]
                color = ColorProfile(color=color,name=name)
                color.save()
                return HttpResponseRedirect(reverse("colors"))
            else:
                return HttpResponse("Ne das läuft nid")
        else:
            form = ColorProfileForm()
            return render(req, "create_color.html",{'form' : form, "head": "New Color", "url" : req.get_full_path()})
    else:
        return HttpResponseRedirect(reverse("login"))