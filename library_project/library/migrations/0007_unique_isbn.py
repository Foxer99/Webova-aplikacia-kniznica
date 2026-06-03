# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_adminactivity_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
