# Generated by Django 2.2.12 on 2021-03-26 13:39

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_s', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='pje_win_cA',
        ),
        migrations.RemoveField(
            model_name='player',
            name='pje_win_cB',
        ),
        migrations.RemoveField(
            model_name='player',
            name='tipo_votante',
        ),
        migrations.AddField(
            model_name='group',
            name='pje_win_cA',
            field=otree.db.models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='pje_win_cB',
            field=otree.db.models.IntegerField(default=0, null=True),
        ),
    ]
