# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LetterRate'
        db.create_table('quinode_shipping_letterrate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('quinode_shipping', ['LetterRate'])

        # Adding M2M table for field regions on 'LetterRate'
        db.create_table('quinode_shipping_letterrate_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('letterrate', models.ForeignKey(orm['quinode_shipping.letterrate'], null=False)),
            ('region', models.ForeignKey(orm['colissimo.region'], null=False))
        ))
        db.create_unique('quinode_shipping_letterrate_regions', ['letterrate_id', 'region_id'])


    def backwards(self, orm):
        
        # Deleting model 'LetterRate'
        db.delete_table('quinode_shipping_letterrate')

        # Removing M2M table for field regions on 'LetterRate'
        db.delete_table('quinode_shipping_letterrate_regions')


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
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['quinode_shipping']
