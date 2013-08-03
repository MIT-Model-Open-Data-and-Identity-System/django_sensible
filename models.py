from django.db import models
from django.contrib.auth.models import User
import time
from hashlib import sha512
from uuid import uuid4

class TimestampGenerator(object):
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds

class KeyGenerator(object):
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]

class Type(models.Model):
        type = models.CharField(max_length=100, db_index=True)
	def __unicode__(self):
		return self.type

class Scope(models.Model):
        scope = models.CharField(unique=True, max_length=100, db_index=True)
        description = models.TextField(blank=True)
	type = models.ForeignKey(Type, blank=True, null=True)
        def __unicode__(self):
                return self.scope

class AccessToken(models.Model):
	user = models.ForeignKey(User)
	token = models.CharField(max_length=100, db_index=True, unique=False)
    	refresh_token = models.CharField(blank=True, null=True, max_length=100)
	scope = models.ManyToManyField(Scope)

class State(models.Model):
	user = models.ForeignKey(User)
	nonce = models.CharField(unique=True, max_length=100, db_index=True, default=KeyGenerator(15))

class Attribute(models.Model):
	scope = models.ForeignKey(Scope)
	attribute = models.CharField(unique=True, max_length=100, db_index=True)
	
class FirstLogin(models.Model):
    user = models.OneToOneField(User)
    firstLogin = models.BooleanField(default=True)

class Cas(models.Model):
	user = models.OneToOneField(User)
	student_id = models.CharField(unique=True, max_length=100, db_index=True)


