from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    contact = models.IntegerField()
    description = models.TextField(blank=True)
    owner = models.IntegerField(blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name
    

class Users(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(null=False)
    phone = models.CharField()

    def __str__ (self):
        return f"{self.firstName} {self.lastName}"
    

class Event(models.Model):
    name = models.CharField(max_length=30)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    eventdate = models.DateField()
    ticketprice = models.DecimalField(decimal_places=2, max_digits=6)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(Users)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = (self.eventdate - today).days
        return days_till
    
    @property
    def Is_past(self):
        today = date.today()
        if self.eventdate < today:
            event = "Event already took place..We made great memories"

        else:
            event = "Event is in the future.See you there"

        return event