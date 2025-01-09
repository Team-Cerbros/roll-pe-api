from django.db import models

from user.models import BaseTimeModel


class PostIt(BaseTimeModel):
	userFK = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

	paperFK = models.ForeignKey('paper.Paper', on_delete=models.CASCADE)

	context = models.TextField()

	danger = models.IntegerField(default=0)

	class Meta:
		verbose_name = 'Postit'

