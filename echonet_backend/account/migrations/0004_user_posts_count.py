from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_friends_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='posts_count',
            field=models.IntegerField(default=0),
        ),
    ]