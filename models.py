from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.




class Query(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    def __str__(self):
        return str(self.question)
