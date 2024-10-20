# Generated by Django 4.1.10 on 2023-12-07 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('level_and_achievement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlevel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_level', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userachievement',
            name='achievement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='level_and_achievement.achievement'),
        ),
        migrations.AddField(
            model_name='userachievement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
