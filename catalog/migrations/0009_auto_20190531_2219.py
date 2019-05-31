# Generated by Django 2.2 on 2019-05-31 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20190523_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('In progress', 'In progress'), ('Ready', 'Ready'), ('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Being tested', 'Being tested')], max_length=15),
        ),
    ]