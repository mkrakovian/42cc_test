# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Request'
        db.create_table(u'contact_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.TextField')()),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('encoding', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user_agent', self.gf('django.db.models.fields.TextField')()),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'contact', ['Request'])


    def backwards(self, orm):
        # Deleting model 'Request'
        db.delete_table(u'contact_request')


    models = {
        u'contact.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'contacts': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'contact.request': {
            'Meta': {'object_name': 'Request'},
            'encoding': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'user_agent': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['contact']