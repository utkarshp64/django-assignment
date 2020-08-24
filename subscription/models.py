from django.db import models


# Create your models here.
class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    started_at = models.TextField(null=True)
    ended_at = models.TextField(null=True)
    canceled_at = models.TextField(null=True)
    status = models.CharField(max_length=50)
    subscription_id = models.TextField()
    product_id = models.TextField()
    price_id = models.TextField()
    user_id = models.TextField()
