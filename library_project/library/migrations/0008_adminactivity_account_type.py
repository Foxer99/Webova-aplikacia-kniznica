# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_unique_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminactivity',
            name='account_type',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
