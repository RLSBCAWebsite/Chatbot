from django.db import models


class Register(models.Model):
    rg_id = models.AutoField(primary_key=True, unique=True)
    rg_name = models.CharField(max_length=100, default="")
    rg_mobile = models.CharField(max_length=100, default="")
    rg_email = models.CharField(max_length=100, default="")
    rg_password = models.CharField(max_length=100, default="")
    rg_status = models.CharField(max_length=100, default="0")

class Contact(models.Model):
    ct_id = models.AutoField(primary_key=True, unique=True)
    ct_name = models.CharField(max_length=100, default="")
    ct_mobile = models.CharField(max_length=100, default="")
    ct_email = models.CharField(max_length=100, default="")
    ct_subject = models.CharField(max_length=100, default="")
    ct_message = models.TextField(default="0")


class Messages(models.Model):
    ms_id = models.AutoField(primary_key=True, unique=True)
    ms_email = models.CharField(max_length=100, default="")
    ms_msg_user = models.CharField(max_length=100, default="")
    ms_msg_bot = models.TextField(default="")
    ms_status = models.CharField(max_length=100, default="0")
