from rest_framework import serializers
from reviews.models import Categorie, Comment, Genre, Review, Title


class TitlesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    description = serializers.StringRelatedField(required=False)
    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='name',
                                          read_only=True)
    
    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        if obj.reviews.count():
            reviews = sum(obj.reviews.values_list("score", flat=True))
            return reviews / obj.reviews.count()
        return None


class CategoriesSerializer(serializers.ModelSerializer):
    titles = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Categorie
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        id_review = self.context['request'].get_full_path().split('/')
        author = self.context['request'].user
        review = Review.objects.filter(
            title=id_review[4]).filter(author=author)
        if review:
            raise serializers.ValidationError(
                'Пользователь может оставить '
                'только один отзыв на произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
