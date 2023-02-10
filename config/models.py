from django.db import models
from .encryption import decrypt_message, encrypt_message
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
User = get_user_model()
# Create your models here.
ORACLE_CONNECTOR_TYPE='oracle'
MYSQL_CONNECTOR_TYPE='mysql'
LDAP_CONNECTOR_TYPE='ldap'
POSTGRE_CONNECTOR_TYPE='postgre/greenplum'
API_CONNECTOR_TYPE='api'
WEBSOURCE_CONNECTOR_TYPE='websource'
class Credential(models.Model):
    name=models.CharField(max_length=150, null=False, default="Credentials")
    username=models.CharField(max_length=50, null=False)
    password=models.TextField(null=False)
    attributes=models.TextField(null=False, default="{}") #store json attributes about the credential

    def save(self, *args, **kwargs):
        self.password = encrypt_message(self.password) #encrypt the password before we save
        super(Credential, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
class Connection(models.Model):
    type=models.CharField(max_length=25,choices=((ORACLE_CONNECTOR_TYPE,ORACLE_CONNECTOR_TYPE), (MYSQL_CONNECTOR_TYPE, MYSQL_CONNECTOR_TYPE), (LDAP_CONNECTOR_TYPE ,LDAP_CONNECTOR_TYPE),(API_CONNECTOR_TYPE ,API_CONNECTOR_TYPE),( POSTGRE_CONNECTOR_TYPE,POSTGRE_CONNECTOR_TYPE), (WEBSOURCE_CONNECTOR_TYPE,WEBSOURCE_CONNECTOR_TYPE)), default=WEBSOURCE_CONNECTOR_TYPE, null=False)
    name=models.CharField(max_length=100, null=False)
    host=models.CharField(max_length=200, null=False)
    port=models.CharField(max_length=5, null=False, default='69')
    credential = models.ForeignKey(Credential,null=True,blank=True, on_delete=models.RESTRICT)
    attributes = models.TextField(null=False, blank=False, default="{}")  # store json attributes about the connection
    def __str__(self):
        return f"{self.name} ({self.type})"

class CodeModel(models.Model):
    name = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=500, null=False, default="Please add a description")
    creation_date = models.DateTimeField(default=now)
    attributes = models.TextField(null=False, default='{}', help_text='json attributes')
    code = models.TextField(null=True, default="print('Hello, world!')",help_text='Python Code To Execute')
    criticality = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])
    class Meta:
       abstract = True




class Configuration(models.Model):#config class, stores kv pairs
    created = models.DateField(null=False, default=now)
    key = models.CharField(max_length=250, null=False)
    value= models.TextField(null=False)
    description=models.TextField(null=False)
    def __str__(self):
        return f"{self.key}"
class NavigationLink(models.Model):
    name=models.CharField(max_length=100, null=False)
    description=models.TextField(null=False)
    location= models.CharField(max_length=500, null=False)
    group = models.ForeignKey("auth.Group", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.location}"

#temporary until sso is enabled. Require everyone to reset their password on initial login
class PasswordResetEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_password_reset = models.DateTimeField(default=now, null=False)