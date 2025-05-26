import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "echonet_backend.settings")
django.setup()


from account.models import SpotifyUser


users = SpotifyUser.objects.all()

for user in users:
    # Clear the suggestion list
    user.people_you_may_know.clear()

    print('Find friends for:', user)

    for friend in user.friends.all():
        print('Is friend with:', friend)

        for friendsfriend in friend.friends.all():
            if friendsfriend not in user.friends.all() and friendsfriend != user:
                user.people_you_may_know.add(friendsfriend)
    
# si el array people_you_may_know no tiene elementos, añadimos usuarios que no sean amigos del usuario loggeado
    if not user.people_you_may_know.exists():
        print('No suggestions found, adding random users')
        random_users = SpotifyUser.objects.exclude(friends__in=[user]).exclude(id=user.id).order_by('?')[:5]
        for random_user in random_users:
            user.people_you_may_know.add(random_user)
    
    print()