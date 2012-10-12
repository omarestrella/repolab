# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Repository.slug'
        db.add_column('repolab_repository', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='slug', unique=True, max_length=64),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Repository.slug'
        db.delete_column('repolab_repository', 'slug')


    models = {
        'repolab.repository': {
            'Meta': {'object_name': 'Repository'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['repolab']