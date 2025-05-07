from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_trend'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]