# Generated by Django 3.1.3 on 2021-06-15 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_remove_course_videos'),
        ('root', '0006_auto_20210615_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.course'),
        ),
    ]