from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Content, Rating
from .serializers import ContentSerializer, RatingSerializer


class ContentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contents = Content.objects.annotate(
            average_rating=Avg('rating__score'),
            rating_count=Count('rating'),
        )
        serializer = ContentSerializer(contents, many=True, context={'request': request})
        return Response(serializer.data)


class ContentDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Content.objects.annotate(
        average_rating=Avg('rating__score'),
        rating_count=Count('rating'),
    )
    serializer_class = ContentSerializer


class RatingCreateUpdateAPIView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'content_id'
    def get_queryset(self):
        user = self.request.user
        content_id = self.kwargs['content_id']
        return Rating.objects.filter(user=user, content_id=content_id)

    def perform_create(self, serializer):
        user = self.request.user
        content_id = self.kwargs['content_id']
        existing_rating = Rating.objects.filter(user=user, content_id=content_id).first()
        if existing_rating:
            raise ValidationError("you already voted")


        serializer.save(user=user, content_id=content_id)

    def perform_update(self, serializer):
        user = self.request.user
        content_id = self.kwargs['content_id']
        rating = Rating.objects.get(user=user, content_id=content_id)
        serializer.save(user=user, content_id=content_id, id=rating.id)
