# Generated by Django 5.2.1 on 2025-07-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionpost',
            name='category',
            field=models.CharField(choices=[('tax', 'Tax'), ('construction', 'Construction'), ('health', 'Health')], default='tax', help_text='Select one: Tax, Construction or Health', max_length=20),
        ),
    ]
