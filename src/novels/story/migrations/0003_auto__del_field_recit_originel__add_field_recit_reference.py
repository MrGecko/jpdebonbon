# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Recit.originel'
        db.delete_column('story_recit', 'originel')

        # Adding field 'Recit.reference'
        db.add_column('story_recit', 'reference', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='recit_reference', null=True, to=orm['story.Recit']), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Recit.originel'
        db.add_column('story_recit', 'originel', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Recit.reference'
        db.delete_column('story_recit', 'reference_id')


    models = {
        'story.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joueur': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'premier_recit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'premier_recit'", 'null': 'True', 'to': "orm['story.Recit']"}),
            'proprietaire': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'titre_url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'story.piste': {
            'Meta': {'object_name': 'Piste'},
            'choix': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'demander': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_karma': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'min_karma': ('django.db.models.fields.IntegerField', [], {'default': '-1000'}),
            'recit_destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destinations'", 'null': 'True', 'to': "orm['story.Recit']"}),
            'recit_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sources'", 'to': "orm['story.Recit']"}),
            'reponse': ('django.db.models.fields.TextField', [], {'max_length': '512', 'blank': 'True'}),
            'texte': ('django.db.models.fields.TextField', [], {'max_length': '512'})
        },
        'story.recit': {
            'Meta': {'object_name': 'Recit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['story.Page']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'recit_reference'", 'null': 'True', 'to': "orm['story.Recit']"})
        }
    }

    complete_apps = ['story']
