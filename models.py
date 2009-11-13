import datetime
from django.db import models


class AqiDefinition(models.Model):
    "EPA definition for AQI"
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    color = models.CharField(max_length=10)
    min_aqi = models.IntegerField()
    max_aqi = models.IntegerField()


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
    tweet_id = models.IntegerField(primary_key=True)
    tweet_timestamp = models.DateTimeField()


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
