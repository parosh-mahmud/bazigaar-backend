# Generated by Django 4.1.10 on 2023-12-07 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_in_group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_reactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='chat_in_community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_in_group.communitychat'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='imagemessage',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_in_group.message'),
        ),
        migrations.AddField(
            model_name='communitymember',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='member', to='chat_in_group.communitychat'),
        ),
        migrations.AddField(
            model_name='communitymember',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
