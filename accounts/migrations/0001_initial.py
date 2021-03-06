# Generated by Django 3.2.6 on 2021-08-12 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rename_file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webex_email', models.EmailField(default=None, max_length=254, null=True)),
                ('profile_pic', models.ImageField(default='default_profile_pic.jpg', upload_to=rename_file.rename_profile_pic)),
                ('city', models.CharField(default='Hyderabad', max_length=100)),
                ('owns_cars', models.BooleanField(default=False, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
