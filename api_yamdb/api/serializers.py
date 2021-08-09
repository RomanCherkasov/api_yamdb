from reviews.models import Titles, Categories, Genres
from rest_framework import serializers


class TitlesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    titles = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Genres
        fields = '__all__'


