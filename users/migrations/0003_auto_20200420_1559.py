# Generated by Django 2.2.6 on 2020-04-20 11:29

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('users', '0002_auto_20200420_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.CharField(max_length=30)),
                ('token', models.UUIDField(null=True)),
                ('contacts_id', django_mysql.models.ListTextField(models.IntegerField(), size=1000)),
                ('gps_id', django_mysql.models.ListTextField(models.IntegerField(), size=1000)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='gp',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='users.Users'),
        ),
        migrations.AlterField(
            model_name='gp_messages',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sendergp', to='users.Users'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='users.Users'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='users.Users'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
