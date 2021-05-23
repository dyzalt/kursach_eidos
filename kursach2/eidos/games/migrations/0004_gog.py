# Generated by Django 3.0.2 on 2021-05-21 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_zaka'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=50, unique=True)),
                ('game_url', models.URLField(unique=True)),
                ('price_amount', models.FloatField(null=True)),
                ('price_currency', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]
