# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_dri.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleImageUploader',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('image', django_dri.fields.ResponsiveImageField(upload_to='images')),
            ],
        ),
    ]
