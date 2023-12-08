from django.shortcuts import render, redirect
from .models import Venue, Event
from django.http import HttpResponseRedirect
from .forms import VenueForm, EventForm, EventAdminForm
from django.http import HttpResponse
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.models import User
import csv


import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator

#generate a pdf file for venue
def venuePdf(request):
    
    #create bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    #designate model
    venues = Venue.objects.all()

    lines = []
    
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.city)
        lines.append("")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

#generate events csv files
def eventCsv(request):
    events = Event.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename=event.csv'

    #create a csv writer
    writer = csv.writer(response)

    writer.writerow(['event name', 'manager', 'event venue', 'event date', 'ticket price'])

    for event in events:
        writer.writerow([event.name, event.manager, event.venue, event.eventdate, event.ticketprice])

    return response

# generate venue text file
def venueText(request):
    venues = Venue.objects.all()
    response = HttpResponse(content_type='text/plain')
    context = 'attachment; filename=venue.txt'
    response['Content-Disposition'] = context

    lines = []
    for venue in venues:
        lines.append(f"{venue.name}\n{venue.address}\n{venue.city}\n\n")
    
    response.writelines(lines)
    return response

def searchVenue(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/searchvenue.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/searchvenue.html', {})
      
def addevent(request):
    submitted = False
    if request.method == 'POST':  # if the form has been submitted
        if request.user.is_superuser:
            form = EventAdminForm(request.POST)
            form.save()
            event = form.save(commit=False)
            if request.user:
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/addevent?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                event = form.save(commit=False)
                if request.user:
                    event.manager = request.user
                    event.save()
                    return HttpResponseRedirect('/addevent?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventAdminForm
        else:
            form = EventForm
            
        if 'submitted' in request.GET:
            submitted = True
        return render(request, 'events/addevent.html', {'form': form, 'submitted': submitted})

def updateEvent(request, id):
    event = Event.objects.get(pk=id)

    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventAdminForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('events')
        else:
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('events')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/updateevent.html', {'event': event, 'form': form})  

def deleteEvent(request, id):
    event = Event.objects.get(pk=id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'event deleted successfully!')
        return redirect('events')
    else:
        messages.success(request, 'you are not authorized to delete this event')
        return redirect('events')

#add event to db
def addvenue(request):
    submitted = False
    if request.method == 'POST': #if the form has been submitted
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            if request.user:
                venue.owner = request.user.id
                venue.save()
                return HttpResponseRedirect('/addvenue?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
        return render(request, 'events/addvenue.html', {'form': form, 'submitted': submitted})

def updateVenue(request, id):
    venue = Venue.objects.get(pk=id)

    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('venues')
    else:
        form = VenueForm(instance=venue)

    return render(request, 'events/updatevenue.html', {'venue': venue, 'form': form})

def deleteVenue(request, id):
    venue = Venue.objects.get(pk=id)
    venue.delete()
    return redirect('venues')

def home(request):
    return render(request, 'events/home.html')

def venues(request):
    myVenues = Venue.objects.all()
    #pagination
    p = Paginator(Venue.objects.all().order_by('name'), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    return render(request, 'events/venues.html', {'venues': myVenues, 'myvenues': venues, 'nums':nums})

def getVenue(request, id):
    venue = Venue.objects.get(pk=id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/venue_details.html', {'venue': venue, 'venue_owner':venue_owner})

def my_events(request):
    if request.user.is_authenticated:
        my_events = Event.objects.filter(manager=request.user.id)
        return render(request, 'events/my_events.html', {'events':my_events})
    else:
        messages.success(request, 'log in to view your events')
        return redirect('home')
def events(request):
    myEvents = Event.objects.all().order_by('name')
    return render(request, 'events/myevents.html', {'events': myEvents})


def adminApproval(request):
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    events = Event.objects.all().order_by('-eventdate')

    if request.user.is_superuser:
        if request.method == "POST":
            id_list = [int(x) for x in request.POST.getlist("boxes")]

            # Uncheck all events
            events.update(approved=False)

            # Update the DB with a single query
            Event.objects.filter(pk__in=id_list).update(approved=True)

            messages.success(request, 'Events list approval has been updated.')
            return redirect('events')
        else:
            return render(request, 'events/adminapproval.html', {
                'events': events,
                'event_count':event_count,
                'venue_count':venue_count,
                'user_count':user_count
                })
    else:
        messages.success(
            request, 'You are not authorized to access this page.')
        return redirect('home')

    return render(request, 'events/adminapproval.html', {})

