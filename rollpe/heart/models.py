from django.db import models
import uuid

from user.models import BaseTimeModel

class Heart(BaseTimeModel):
	userFK = models.ForeignKey(
     	'user.User', 
      	on_delete=models.DO_NOTHING
	)
	paperFK = models.ForeignKey(
    	'paper.Paper', 
    	on_delete=models.CASCADE
    )
	code = models.UUIDField(
    	default=uuid.uuid4, 
    	editable=True,
    	null=True 
	)
	danger = models.IntegerField(
		default=0
	)
	context = models.TextField()
 
	class Meta:
		verbose_name = 'heart'
  