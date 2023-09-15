from rest_framework import serializers
from applications.films.models import Rating, Film, Like, Comment


class LikeSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='Like')

    class Meta:
        model = Like
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    def to_representation(self, instance):

        rep = super().to_representation(instance)
        rep['like_count'] = instance.likes.filter(is_like=True).count()
        rating_result = 0

        for rating in instance.ratings.all():
            rating_result += rating.rating
        if rating_result:
            rep['rating'] = rating_result / instance.ratings.all().count()
        else:
            rep['rating'] = 0
        return rep

    class Meta:

        model = Film
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('rating',)



class CommentsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'