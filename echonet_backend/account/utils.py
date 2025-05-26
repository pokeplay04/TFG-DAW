from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

import requests
from django.conf import settings

def refresh_spotify_token(user):
    refresh_token = user.refresh_token

    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    })

    if response.status_code == 200:
        tokens = response.json()
        user.access_token = tokens['access_token']
        user.save()
        return user.access_token
    else:
        raise Exception("No se ha podido obtener refresh_token de Spotify")


def get_valid_access_token(user):
    try:
        return refresh_spotify_token(user)
    except:
        return user.access_token  # si aún no ha expirado



def crop_center_square(image):
    img = Image.open(image)
    width, height = img.size
    min_dim = min(width, height)

    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2

    img_cropped = img.crop((left, top, right, bottom))

    # Convert to RGB to avoid issues with PNGs with transparency
    if img_cropped.mode in ("RGBA", "P"):
        img_cropped = img_cropped.convert("RGB")

    buffer = BytesIO()
    img_cropped.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

