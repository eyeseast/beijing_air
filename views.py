import csv
import datetime

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from beijing_air.models import AqiDefinition, SmogUpdate

DEFAULT_RANGE = 30

def get_range(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    
    if end:
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    else:
        end_date = datetime.datetime.now()
    
    if start:
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    else:
        start_date = end_date - datetime.timedelta(DEFAULT_RANGE)
    
    return start_date, end_date


def index(request):
    start, end = get_range(request)
    updates = SmogUpdate.objects.range(start, end)
    today = SmogUpdate.objects.daily_avg()
    definition = AqiDefinition.objects.get(min_aqi__lt=today, max_aqi__gt=today)
    average = updates.aggregate(aqi=Avg('aqi'))['aqi']
    return render_to_response("beijing_air/index.html", locals(), context_instance=RequestContext(request))


def timeplot_csv(request):
    "Generates a CSV using range defined in request params"
    start, end = get_range(request)
    
    updates = SmogUpdate.objects.range(start, end)
    
    response = HttpResponse(mimetype='text/plain')
    writer = csv.writer(response)
    
    for update in updates:
        writer.writerow([update.timestamp, update.concentration, update.aqi, update.definition])
    
    return response