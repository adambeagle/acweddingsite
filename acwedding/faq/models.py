from django.db import models

class Entry(models.Model):
    
    # Note id is explicit here so it can be easily edited via the
    # admin site. The order questions appear is based on the id
    # field; It's likely a user may want to edit that order.
    id = models.PositiveSmallIntegerField(primary_key=True)
    question = models.CharField(max_length=75)
    answer = models.TextField()

    def __str__(self):
        return "{0} - {1}".format(str(self.id), str(self.question))
        
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Entries'

