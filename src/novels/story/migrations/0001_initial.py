# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('story_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('titre_url', self.gf('django.db.models.fields.CharField')(default='<django.db.model', max_length=32)),
            ('proprietaire', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('joueur', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('premier_recit', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='premier_recit', null=True, to=orm['story.Recit'])),
        ))
        db.send_create_signal('story', ['Page'])

        # Adding model 'Recit'
        db.create_table('story_recit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['story.Page'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('karma', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('originel', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('story', ['Recit'])

        # Adding model 'Piste'
        db.create_table('story_piste', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recit_source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sources', to=orm['story.Recit'])),
            ('recit_destination', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='destinations', null=True, to=orm['story.Recit'])),
            ('texte', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('choix', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('demander', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reponse', self.gf('django.db.models.fields.TextField')(max_length=512, blank=True)),
            ('karma', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('min_karma', self.gf('django.db.models.fields.IntegerField')(default=-1000)),
            ('max_karma', self.gf('django.db.models.fields.IntegerField')(default=1000)),
        ))
        db.send_create_signal('story', ['Piste'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('story_page')

        # Deleting model 'Recit'
        db.delete_table('story_recit')

        # Deleting model 'Piste'
        db.delete_table('story_piste')


    models = {
        'story.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joueur': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'premier_recit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'premier_recit'", 'null': 'True', 'to': "orm['story.Recit']"}),
            'proprietaire': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'titre_url': ('django.db.models.fields.CharField', [], {'default': "'<django.db.model'", 'max_length': '32'})
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
            'originel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['story.Page']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['story']
