# Generated by Django 3.1.3 on 2021-05-16 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_delete_stream'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(default='ok', max_length=200),
            preserve_default=False,
        ),
    ]
