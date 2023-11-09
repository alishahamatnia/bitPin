from rest_framework import serializers
from .models import Content, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']


class ContentSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    rating_count = serializers.IntegerField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'text', 'average_rating', 'rating_count', 'user_rating']

    def get_user_rating(self, obj):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.filter(user=user, content=obj).first()
        if rating:
            return RatingSerializer(rating).data
        return None
