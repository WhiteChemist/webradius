from django.db import models

# Create your models here.
class radacct(models.Model):
    AcctSessionId = models.TextField()
    AcctUniqueID = models.TextField(unique=True)
    UserName = models.TextField()
    GroupName = models.TextField()
    Realms = models.TextField()
    NASIPAddress = models.IPAddressField()
    NASPortId = models.TextField()
    NASPortType = models.TextField()
    AcctStartTime = models.DateTimeField()
    AcctUpdateTime = models.DateTimeField()
    AcctStopTime = models.DateTimeField()
    AcctInterval = models.BigIntegerField()
    AcctSessionTime = models.BigIntegerField()
    AcctAuthentic = models.TextField()
    ConnectInfoStart = models.TextField()
    ConnectInfoStop = models.TextField()
    AcctInputOctets = models.BigIntegerField()
    AcctOutputOctets = models.BigIntegerField()
    CalledStationId = models.TextField()
    CallingStationId = models.TextField()
    AcctTerminateCause = models.TextField()
    ServiceType = models.TextField()
    FramedProtocol = models.TextField()
    FramedIPAddress = models.IPAddressField()
    FramedIPv6Address = models.IPAddressField()
    FramedIPv6Prefix = models.IPAddressField()
    FramedInterfaceId = models.TextField()
    DelegatedIPv6Prefix = models.TextField()
    Class = models.TextField()

class radcheck(models.Model):
    UserName = models.TextField(null=False,default='',)
    Attribute = models.TextField(null=False,default='')
    op = models.CharField(max_length=2,null=False,default='==')
    Value = models.TextField(null=False,default='')

class radgroupcheck(models.Model):
    GroupName = models.TextField(null=False,default='')
    Attribute = models.TextField(null=False,default='')
    op = models.CharField(max_length=2,null=False,default='==')
    Value = models.TextField(null=False,default='')

class radgroupreply(models.Model):
    GroupName = models.TextField(null=False,default='')
    Attribute = models.TextField(null=False,default='')
    op = models.CharField(max_length=2,null=False,default='==')
    Value = models.TextField(null=False,default='')

class radreply(models.Model):
    UserName = models.TextField(null=False,default='',)
    Attribute = models.TextField(null=False,default='')
    op = models.CharField(max_length=2,null=False,default='==')
    Value = models.TextField(null=False,default='')

class radusergroup(models.Model):
    UserName = models.TextField(null=False,default='',db_index=True)
    GroupName = models.TextField(null=False,default='',)
    priority = models.IntegerField(null=False,default=0)

class radpostauth(models.Model):
    username = models.TextField(null=False)
    password = models.TextField()
    reply = models.TextField()
    CalledStationId = models.TextField()
    CallingStationId = models.TextField()
    authdate = models.DateTimeField(null=False,default='now()')
    Class = models.TextField()

class nas(models.Model):
    nasname = models.TextField(null=False,db_index=True)
    shortname = models.TextField(null=False)
    type = models.TextField(null=False,default='Mikrotik')
    ports = models.IntegerField()
    secret = models.TextField(null=False)
    server = models.TextField()
    community = models.TextField()
    description = models.TextField()

class nasreload(models.Model):
    NASIPAddress = models.IPAddressField(primary_key=True)
    ReloadTime = models.DateTimeField(null=False)