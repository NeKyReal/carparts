# Generated by Django 5.0.7 on 2024-07-18 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('producer_country_name', models.CharField(max_length=100)),
                ('is_visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_visible', models.BooleanField(default=True)),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.mark')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('price', models.IntegerField()),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('is_visible', models.BooleanField(db_index=True, default=True)),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.mark')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.model')),
            ],
            options={
                'indexes': [models.Index(fields=['name', 'mark', 'price'], name='parts_part_name_956e0f_idx'), models.Index(fields=['json_data'], name='parts_part_json_da_f33736_idx')],
            },
        ),
    ]