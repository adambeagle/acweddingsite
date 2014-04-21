from django.db import models

class Entry(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    question = models.CharField(max_length=75)
    answer = models.TextField()

    def __str__(self):
        return "{0} - {1}".format(str(self.id), str(self.question))

