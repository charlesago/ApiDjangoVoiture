# Generated by Django 3.2.12 on 2024-10-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0005_globalapikey_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('api_key', models.CharField(max_length=256, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
