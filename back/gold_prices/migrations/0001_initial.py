# Generated by Django 4.2.21 on 2025-05-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetalPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal_type', models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver')], max_length=10)),
                ('date', models.DateField()),
                ('close_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('metal_type', 'date')},
            },
        ),
    ]
