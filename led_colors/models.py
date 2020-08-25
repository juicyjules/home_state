from django.db import models
from django.conf import settings
import uuid
# Create your models here.
class ColorProfile(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(default="ffffffff",max_length=8)
    function = models.TextField(null=True,blank=True)
    period_time = models.IntegerField(default=0)
    def __str__(self):
        return "#"+str(self.color.upper())

class ClientManager(models.Manager):
    def clients_for_user_id(self,user_id):
        return super().get_queryset().filter(owner__id=user_id)
    def clients_for_user(self,user):
        user.client_set.all()
    def get_client_for_key(self,key):
        return super().get_queryset().filter(key=key).first()
    def set_master_color(self,user_id,profile_id):
        for client in super().get_queryset().filter(owner__id=user_id):
            client.current_profile_id = profile_id
            client.save()
    def turn_on(self,user_id,on):
        for client in super().get_queryset().filter(owner__id=user_id):
            client.on = on
            client.save()

class Client(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    ip = models.BinaryField(default=bytes(0),max_length=4)
    last_connection = models.DateTimeField(null=True,blank=True)
    current_profile = models.ForeignKey(ColorProfile,on_delete=models.DO_NOTHING,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    on = models.BooleanField(default=False)
    
    manager = ClientManager()

    def __str__(self):
        return self.name+"::"+str(self.key)