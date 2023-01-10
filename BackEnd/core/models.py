from django.db import models

class Client(models.Model):
    name= models.CharField(max_length=100, unique=True, db_column='CreCliNme')
    
    class Meta:
        db_table= 'CreCli'

    def __str__(self) -> str:
        return self.name