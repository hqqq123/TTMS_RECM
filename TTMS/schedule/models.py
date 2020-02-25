from django.db import models

# Create your models here.
from django.utils import timezone

from play.models import Play
from studio.models import Studio


class Schedule(models.Model):

    play=models.ForeignKey(Play,on_delete=models.SET_NULL,null=True)
    studio=models.ForeignKey(Studio,on_delete=models.SET_NULL,null=True)
    show_time=models.DateTimeField()
    end_time=models.DateTimeField()
    ticket_counts=models.IntegerField()#剩余票数
    ticket_all_counts=models.IntegerField()

    ticket_money=models.FloatField(default=40)
    status = models.IntegerField(default=1)  # 1:正在上映，0：已下架

    # order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)