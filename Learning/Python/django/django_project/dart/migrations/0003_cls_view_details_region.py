# Generated by Django 3.0.8 on 2020-07-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dart', '0002_auto_20200723_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='cls_view_details',
            name='region',
            field=models.CharField(default='HK', max_length=10),
            preserve_default=False,
        ),
    ]
