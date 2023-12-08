from django.db import models

# Create your models here.


class Menu(models.Model):
    foodtype = models.CharField(max_length=50)
    foodname = models.CharField(max_length=50)
    foodprice = models.FloatField()
    foodquantity = models.IntegerField()
    fooddescription = models.TextField()
    foodimage = models.ImageField(blank=True, null=True, upload_to='images2/')

    def __str__(self):
        return f'{self.foodname} {self.foodtype}'

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menus'

