# Generated by Django 2.2.7 on 2020-01-12 21:32

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_wallets.wallet_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='CommerceWallet',
            fields=[
                ('wallet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallets.Wallet')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wallets.wallet',),
        ),
        migrations.CreateModel(
            name='CustomerWallet',
            fields=[
                ('wallet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallets.Wallet')),
            ],
            options={
                'ordering': ['customer'],
            },
            bases=('wallets.wallet',),
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('type', models.CharField(choices=[('1', 'Pending'), ('2', 'Done'), ('3', 'Error')], default='1', max_length=10)),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Done'), ('3', 'Error')], default='1', max_length=10)),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('from_wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_operations', to='wallets.Wallet')),
                ('to_wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_operations', to='wallets.Wallet')),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.AddIndex(
            model_name='operation',
            index=models.Index(fields=['to_wallet', 'from_wallet'], name='wallets_ope_to_wall_5ff8ac_idx'),
        ),
        migrations.AddField(
            model_name='customerwallet',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to='users.Customer'),
        ),
        migrations.AddField(
            model_name='commercewallet',
            name='commerce',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='users.Commerce'),
        ),
        migrations.AddIndex(
            model_name='customerwallet',
            index=models.Index(fields=['customer'], name='wallets_cus_custome_19ca51_idx'),
        ),
    ]
