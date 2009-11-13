
from south.db import db
from django.db import models
from beijing_air.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AqiDefinition'
        db.create_table('beijing_air_aqidefinition', (
            ('id', orm['beijing_air.AqiDefinition:id']),
            ('name', orm['beijing_air.AqiDefinition:name']),
            ('slug', orm['beijing_air.AqiDefinition:slug']),
            ('color', orm['beijing_air.AqiDefinition:color']),
            ('min_aqi', orm['beijing_air.AqiDefinition:min_aqi']),
            ('max_aqi', orm['beijing_air.AqiDefinition:max_aqi']),
        ))
        db.send_create_signal('beijing_air', ['AqiDefinition'])
        
        # Adding model 'SmogUpdate'
        db.create_table('beijing_air_smogupdate', (
            ('timestamp', orm['beijing_air.SmogUpdate:timestamp']),
            ('aqi', orm['beijing_air.SmogUpdate:aqi']),
            ('concentration', orm['beijing_air.SmogUpdate:concentration']),
            ('definition', orm['beijing_air.SmogUpdate:definition']),
            ('tweet_id', orm['beijing_air.SmogUpdate:tweet_id']),
            ('tweet_timestamp', orm['beijing_air.SmogUpdate:tweet_timestamp']),
        ))
        db.send_create_signal('beijing_air', ['SmogUpdate'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AqiDefinition'
        db.delete_table('beijing_air_aqidefinition')
        
        # Deleting model 'SmogUpdate'
        db.delete_table('beijing_air_smogupdate')
        
    
    
    models = {
        'beijing_air.aqidefinition': {
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'tweet_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'tweet_timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }
    
    complete_apps = ['beijing_air']
