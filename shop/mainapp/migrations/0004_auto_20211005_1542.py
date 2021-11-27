# Generated by Django 3.2.7 on 2021-10-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_somemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SomeModel',
        ),
        migrations.AlterField(
            model_name='notebookproduct',
            name='warranty',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Гарантия'),
        ),
        migrations.AlterField(
            model_name='smartphoneproduct',
            name='warranty',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Гарантия'),
        ),
    ]
