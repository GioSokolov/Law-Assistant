# Generated by Django 5.1.1 on 2024-12-02 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legal', '0006_article_articlecomment_articlelike'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='articles/documents/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]