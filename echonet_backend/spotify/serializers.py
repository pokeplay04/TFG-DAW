from rest_framework import serializers

class SpotifyTrackSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    artist = serializers.CharField()
    image = serializers.URLField(allow_blank=True)

class SpotifyAlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    artist = serializers.CharField()
    image = serializers.URLField(allow_blank=True)


class SpotifyArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    image = serializers.URLField(allow_blank=True)
