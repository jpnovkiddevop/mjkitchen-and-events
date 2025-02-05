from django.contrib import admin
from .models import Venue, User, Event

#Register your models here.
#admin.site.register(Venue)
#admin.site.register(User)
#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name','city', 'address')
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'), 'eventdate', 'manager','ticketprice' , 'approved')
    list_display = ('name', 'eventdate', 'venue', 'ticketprice')
    list_filter = ('eventdate', 'venue')
    ordering = ('eventdate', )
