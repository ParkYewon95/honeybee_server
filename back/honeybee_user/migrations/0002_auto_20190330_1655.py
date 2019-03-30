# Generated by Django 2.1.7 on 2019-03-30 07:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('honeybee_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='honeybeeuser',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='pk_id'),
        ),
        migrations.AlterField(
            model_name='honeybeeuser',
            name='id',
            field=models.CharField(max_length=20, unique=True, verbose_name='아이디'),
        ),
    ]
