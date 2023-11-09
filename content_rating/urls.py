from django.urls import path
from .views import ContentListAPIView, ContentDetailAPIView, RatingCreateUpdateAPIView

urlpatterns = [
    path('', ContentListAPIView.as_view(), name='content-list'),
    path('<int:pk>/', ContentDetailAPIView.as_view(), name='content-detail'),
    path('<int:content_id>/rating/', RatingCreateUpdateAPIView.as_view(), name='rating-create-update'),
]