# Generated by Django 4.1.10 on 2024-10-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_remove_walletbankaccounts_wallet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bonusbgcoin',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
