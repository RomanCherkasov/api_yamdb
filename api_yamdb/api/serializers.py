from rest_framework import serializers
from reviews.models import Categories, Comment, Genres, Review, Title


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesWriteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Categories.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genres.objects.all(),
                                         many=True)
    
    class Meta:
        model = Title
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True)
    rating = serializers.SerializerMethodField(required=False)
    
    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        if obj.reviews.count(): 
            reviews = sum(obj.reviews.values_list("score", flat=True))
            return reviews / obj.reviews.count()
        return None
    

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
