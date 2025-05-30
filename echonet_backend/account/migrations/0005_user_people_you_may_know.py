from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_posts_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='people_you_may_know',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]