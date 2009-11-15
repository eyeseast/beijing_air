import datetime
from django.db import models
from django.db.models import Avg

#
# Managers
#

class SmogManager(models.Manager):
    def get_earliest_update(self):
        """returns the earliest SmogUpdate in the database, or None"""
        updates = self.order_by('timestamp')
        try:
            return updates[0]
        except IndexError: # no updates yet
            return None
    
    
    def range(self, start, end):
        """Returns all updates between two dates"""
        return self.filter(
            timestamp__gt=start,
            timestamp__lt=end
        )
    
    def date(self, day):
        return self.filter(
            timestamp__year=day.year,
            timestamp__month=day.month,
            timestamp__day=day.day
        )
    
    def daily_avg(self, day=None, field='aqi'):
        if not day:
            day = datetime.datetime.today()
        return self.date(day).aggregate(Avg(field))['%s__avg' % field]


#
# Models
#

class AqiDefinition(models.Model):
    "EPA definition for AQI"
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    color = models.CharField(max_length=10)
    min_aqi = models.IntegerField()
    max_aqi = models.IntegerField()
    description = models.TextField(blank=True)


    class Meta:
        ordering = ('min_aqi',)


    def __unicode__(self):
        return self.name


class SmogUpdate(models.Model):
    """Simple model storing AQI updates from
    the US embassy in Beijing, which tracks
    PM2.5 concentrations.
    """
    timestamp = models.DateTimeField()
    aqi = models.IntegerField()
    concentration = models.DecimalField(max_digits=4, decimal_places=3)
    definition = models.ForeignKey(AqiDefinition, related_name="updates")

    # twitter metadata
    tweet_id = models.CharField(max_length=30)
    tweet_timestamp = models.DateTimeField()

    objects = SmogManager()


    class Meta:
        get_latest_by = "timestamp"
        ordering = ('-timestamp',)


    def __unicode__(self):
        return u"%s: %s - %s" % (self.timestamp, self.aqi, self.definition.name)


    def check_definition(self):
        d = AqiDefinition.objects.get(
            min_aqi__lt=self.aqi,
            max_aqi__gt=self.aqi
        )
        return d
