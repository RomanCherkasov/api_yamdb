from rest_framework import serializers
from reviews.models import Categories, Comment, Genres, Review, Title
from rest_framework.serializers import UniqueTogetherValidator


class TitlesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    description = serializers.StringRelatedField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        if obj.reviews.count():
            reviews = sum(obj.reviews.values_list("score", flat=True))
            return reviews / obj.reviews.count()
        return 0


class CategoriesSerializer(serializers.ModelSerializer):
    titles = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    # titles = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Genres
        fields = ('name', 'slug')
        read_only_fields = ('title',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        # fields = '__all__'
        read_only_fields = ('title',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title', 'author'),
        #         message="Возможен только один отзыв!"
        #     )
        # ]

    # def validate(self, data):
    #     id_review = self.context['request'].get_full_path().split('/')
    #     author = self.context['request'].user
    #     review = Review.objects.filter(
    #         title=id_review[4]).filter(author=author)
    #     if review:
    #         raise serializers.ValidationError(
    #             'Пользователь может оставить '
    #             'только один отзыв на произведение!'
    #         )
    #     return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
