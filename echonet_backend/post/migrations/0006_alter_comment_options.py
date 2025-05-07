from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_post_comments_count_comment_post_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]