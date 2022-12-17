# Generated by Django 4.1.3 on 2022-11-20 18:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]