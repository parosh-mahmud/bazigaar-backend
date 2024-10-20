# Generated by Django 4.1.10 on 2024-10-07 13:57

import base.base
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=55)),
                ('status', models.CharField(default='Pending', max_length=55)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='MobileBankWithdrawalRequet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=10)),
                ('bankName', models.CharField(max_length=27)),
                ('number', models.CharField(max_length=27)),
                ('withdrawalRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_app.withdrawalrequest')),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='MobileBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('bankName', models.CharField(max_length=50)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_app.wallet')),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='CryptoWithdrawalRequet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('networkName', models.CharField(max_length=50)),
                ('cryptoName', models.CharField(max_length=50)),
                ('withdrawalRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_app.withdrawalrequest')),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('networkName', models.CharField(max_length=50)),
                ('cryptoName', models.CharField(max_length=50)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_app.wallet')),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='BankWithdrawalRequet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=10)),
                ('accountNumber', models.CharField(max_length=250)),
                ('accountHolderName', models.CharField(max_length=250)),
                ('bankName', models.CharField(max_length=250)),
                ('branchName', models.CharField(max_length=250)),
                ('withdrawalRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_app.withdrawalrequest')),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNumber', models.CharField(max_length=250)),
                ('accountHolderName', models.CharField(max_length=250)),
                ('bankName', models.CharField(max_length=250)),
                ('branchName', models.CharField(max_length=250)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_app.wallet')),
            ],
            bases=(models.Model, base.base.SerializedModel),
        ),
    ]
