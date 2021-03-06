from django.db import models

# Create your models here.
from studio.models import Studio
from type.models import Type



class Play(models.Model):

    name=models.CharField(max_length=50,db_index=True)
    play_time=models.DateField()
    length=models.IntegerField()
    desc=models.TextField()
    director=models.CharField(max_length=20)
    actors=models.CharField(max_length=100)
    area=models.CharField(max_length=20)
    score=models.FloatField(default=0.0)
    img = models.CharField(max_length=200,null=True)

    types=models.ManyToManyField(Type)
    status = models.IntegerField(default=1)  # 1:正在上映，0：已下架
    # studios=models.ManyToManyField(Studio)

