from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    # auto_now_add는 model이 생성된 날짜를 기록하고, auto_now는 업데이트(수정)된 날짜를 기록한다.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # abstact model is a model but doesn't go to database
        abstract = True
