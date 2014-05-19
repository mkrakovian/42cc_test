# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'contact_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('birth', self.gf('django.db.models.fields.DateField')()),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('jabber', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contacts', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'contact', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'contact_person')


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
        }
    }

    complete_apps = ['contact']