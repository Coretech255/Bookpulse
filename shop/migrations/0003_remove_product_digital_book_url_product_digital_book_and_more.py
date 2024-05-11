# Generated by Django 5.0.2 on 2024-04-28 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_digital_book_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital_book_url',
        ),
        migrations.AddField(
            model_name='product',
            name='digital_book',
            field=models.FileField(blank=True, null=True, upload_to='books/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.ImageField(upload_to=''),
        ),
    ]
