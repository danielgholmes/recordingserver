# Generated by Django 2.2.11 on 2020-03-14 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='filename',
            field=models.CharField(default='test.txt', max_length=256),
            preserve_default=False,
        ),
    ]
