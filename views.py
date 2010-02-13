import csv
import datetime
import dateutil.parser

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from beijing_air import utils
from beijing_air.forms import DateRangeForm
from beijing_air.models import AqiDefinition, SmogUpdate


def index(request):
    if request.GET:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start, end = utils.get_range(form.cleaned_data)
        else:
            start, end = utils.get_range({})
            
    else:
        form = DateRangeForm()
        start, end = utils.get_range({})
        
    updates = SmogUpdate.objects.range(start, end)
    today = SmogUpdate.objects.daily_avg()
    definition = AqiDefinition.objects.get(min_aqi__lt=today, max_aqi__gte=today)
    average = updates.aggregate(aqi=Avg('aqi'))['aqi']
    return render_to_response("beijing_air/index.html", locals(), context_instance=RequestContext(request))


def timeplot_csv(request):
    "Generates a CSV using range defined in request params"
    start, end = utils.get_range(request.GET)
    
    updates = SmogUpdate.objects.range(start, end)
    
    response = HttpResponse(mimetype='text/plain')
    response.write("# timestamp, concentration, aqi, definition \n")
    writer = csv.writer(response)
    
    for update in updates:
        writer.writerow([update.timestamp, update.concentration, update.aqi, update.definition])
    
    return response
