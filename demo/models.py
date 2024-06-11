from django.db import models

class Floor(models.Model):
    floor_number=models.IntegerField()
    alphabet_series=models.CharField(max_length=100)
class Slot(models.Model):
    floor=models.ForeignKey(Floor,on_delete=models.CASCADE)
    slot_number=models.IntegerField()
    status=models.BooleanField(default=False)
    


