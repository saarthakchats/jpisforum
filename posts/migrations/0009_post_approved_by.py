# Generated by Django 2.1 on 2019-08-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_post_approvals'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='approved_by',
            field=models.TextField(default=''),
        ),
    ]
