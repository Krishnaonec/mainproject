# Generated by Django 3.2.6 on 2021-08-17 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webexmint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webex_email', models.EmailField(default=None, max_length=254, null=True)),
                ('webex_id', models.TextField(default=None, null=True)),
                ('access_token', models.TextField(default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserToken',
        ),
    ]
