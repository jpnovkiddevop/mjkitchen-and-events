from django import forms
from django.forms import ModelForm
from .models import Venue, Event

class VenueForm(ModelForm):
    class Meta:
        model = Venue

        fields = ('name','address', 'city', 'contact', 'description', 'venue_image')

        labels = {
            'name': '',
            'address': '',
            'city': '',
            'contact': '',
            'description': '',
            'venue_image': '',
        }

        widgets = {
            'name': forms.TextInput({'class': 'form-control', 'placeholder': 'venue name'}),
            'address': forms.TextInput({'class': 'form-control', 'placeholder': 'address'}),
            'city': forms.TextInput({'class': 'form-control', 'placeholder': 'city'}),
            'contact': forms.TextInput({'class': 'form-control', 'placeholder': 'contact'}),
            'description': forms.Textarea({'class': 'form-control mytextarea', 'placeholder': 'description'}),
        }
# admin event form
class EventAdminForm(ModelForm):
    class Meta:
        model = Event

        fields = ('name', 'venue', 'eventdate', 'ticketprice', 'manager')

        labels = {
               'name': '',
               'venue': '',
               'eventdate': 'yy:mm:dd',
               'ticketprice': '',
               'manager': 'manager',
        }

        widgets = {
            'name': forms.TextInput({'class': 'form-control', 'placeholder': 'event name'}),
            'venue': forms.Select({'class': 'form-control', 'placeholder': 'venue'}),
            'eventdate': forms.TextInput({'class': 'form-control', 'placeholder': 'eventdate'}),
            'ticketprice': forms.TextInput({'class': 'form-control', 'placeholder': 'ticketprice'}),
            'manager': forms.Select({'class': 'form-select', 'placeholder': 'manager'}),
        }
#user event form
class EventForm(ModelForm):
    class Meta:
        model = Event

        fields = ('name', 'venue', 'eventdate', 'ticketprice')

        labels = {
               'name': '',
               'venue': '',
               'eventdate': 'yy:mm:dd',
               'ticketprice': '',
        }

        widgets = {
            'name': forms.TextInput({'class': 'form-control', 'placeholder': 'event name'}),
            'venue': forms.Select({'class': 'form-control', 'placeholder': 'venue'}),
            'eventdate': forms.TextInput({'class': 'form-control', 'placeholder': 'eventdate'}),
            'ticketprice': forms.TextInput({'class': 'form-control', 'placeholder': 'ticketprice'}),
        }
