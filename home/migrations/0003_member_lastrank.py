# Generated by Django 2.1.5 on 2019-01-30 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='lastrank',
            field=models.IntegerField(default=1),
        ),
    ]
