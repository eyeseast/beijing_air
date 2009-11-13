
from south.db import db
from django.db import models
from beijing_air.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'SmogUpdate.tweet_id'
        # (to signature: django.db.models.fields.CharField(max_length=30))
        db.alter_column('beijing_air_smogupdate', 'tweet_id', orm['beijing_air.smogupdate:tweet_id'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'SmogUpdate.tweet_id'
        # (to signature: django.db.models.fields.CharField(max_length=20))
        db.alter_column('beijing_air_smogupdate', 'tweet_id', orm['beijing_air.smogupdate:tweet_id'])
        
    
    
    models = {
        'beijing_air.aqidefinition': {
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_aqi': ('django.db.models.fields.IntegerField', [], {}),
            'min_aqi': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'beijing_air.smogupdate': {
            'aqi': ('django.db.models.fields.IntegerField', [], {}),
            'concentration': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '3'}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updates'", 'to': "orm['beijing_air.AqiDefinition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'tweet_timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }
    
    complete_apps = ['beijing_air']
