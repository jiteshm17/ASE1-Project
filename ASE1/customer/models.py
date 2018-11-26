from django.db import models
from django.contrib.auth.models import User
from vendor.models import Product
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator

# def phone_number_validate(phone_number):
#
#     if len(str(phone_number)) != 10:
#         raise ValueError('Phone number must have length 10')


class CustomerProfile(models.Model):
    Customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cus')
    phone_number = models.IntegerField(null=True, validators=[MaxValueValidator(9999999999)])
    address = models.TextField(null=True)

    def __str__(self):
        return self.Customer.username


def post_save_customerprofile_create(sender, instance, created, *args, **kwargs):
    if created:
        CustomerProfile.objects.get_or_create(Customer=instance)


post_save.connect(post_save_customerprofile_create, sender=User)
