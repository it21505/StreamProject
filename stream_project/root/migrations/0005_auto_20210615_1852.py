# Generated by Django 3.1.3 on 2021-06-15 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0004_auto_20210612_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='stream_key',
            field=models.CharField(max_length=200),
        ),
    ]
