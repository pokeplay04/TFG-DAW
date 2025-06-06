from rest_framework import serializers

class SpotifyTrackSerializer(serializers.Serializer):
    id = serializers.CharField()
    track_id = serializers.CharField()
    track_name = serializers.CharField()
    track_artist = serializers.CharField()
    track_image = serializers.URLField(allow_blank=True)
    track_url = serializers.URLField(allow_blank=True)

class SpotifyAlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    album_id = serializers.CharField()
    album_name = serializers.CharField()
    album_artist = serializers.CharField()
    album_image = serializers.URLField(allow_blank=True)
    album_url = serializers.URLField(allow_blank=True)

class SpotifyArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    artist_id = serializers.CharField()
    artist_name = serializers.CharField()
    artist_image = serializers.URLField(allow_blank=True)
    artist_url = serializers.URLField(allow_blank=True)
