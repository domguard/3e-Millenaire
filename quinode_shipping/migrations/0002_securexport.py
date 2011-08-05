# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'LetterRate.securexport'
        db.add_column('quinode_shipping_letterrate', 'securexport', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=5, decimal_places=2), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'LetterRate.securexport'
        db.delete_column('quinode_shipping_letterrate', 'securexport')


    models = {
        'colissimo.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'quinode_shipping.letterrate': {
            'Meta': {'object_name': 'LetterRate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['colissimo.Region']", 'symmetrical': 'False'}),
            'securexport': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '5', 'decimal_places': '2'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['quinode_shipping']
