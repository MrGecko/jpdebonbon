# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Page.premier_recit'
        db.alter_column('story_page', 'premier_recit_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['story.Recit']))


    def backwards(self, orm):
        
        # Changing field 'Page.premier_recit'
        db.alter_column('story_page', 'premier_recit_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['story.Recit']))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'story.page': {
            'Meta': {'unique_together': "(('titre_url', 'proprietaire', 'joueur'),)", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joueur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joueur'", 'to': "orm['auth.User']"}),
            'premier_recit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'premier_recit'", 'null': 'True', 'to': "orm['story.Recit']"}),
            'proprietaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proprietaire'", 'to': "orm['auth.User']"}),
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
            'publication_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['story']
