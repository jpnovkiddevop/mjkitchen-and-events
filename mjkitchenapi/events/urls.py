from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('venues/', views.venues, name='venues'),
   # path('users/', views.users, name='users'),
    path('addvenue/', views.addvenue, name='addvenue'),
    path('addevent/', views.addevent, name='addevent'),
    path('venues/getVenue/<int:id>', views.getVenue, name='venue'),
    path('searchVenue/', views.searchVenue, name='search-venue'),
    path('venues/updateVenue/<int:id>', views.updateVenue, name='update-venue'),
    path('venues/updateEvent/<int:id>', views.updateEvent, name='update-event'),
    path('deleteEvent/<int:id>', views.deleteEvent, name='delete-event'),
    path('deleteVenue/<int:id>', views.deleteVenue, name='delete-venue'),
    path('venueText/', views.venueText, name='venue-text'),
    path('eventCsv/', views.eventCsv, name='event-csv'),
    path('venuePdf/', views.venuePdf, name='venue-pdf'),
    path('my_events/', views.my_events, name='my-events'),
    path('adminApproval/', views.adminApproval, name='admin-approval')
]