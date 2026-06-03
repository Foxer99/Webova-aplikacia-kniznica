# Generated manually to keep activity names after account deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_adminactivity_keep_deleted_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminactivity',
            name='account_name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
