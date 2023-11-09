from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from content_rating.models import Rating, Content


class RatingCreateUpdateAPIViewTest(TestCase):
    def setUp(self):
        content = Content.objects.create(text="test content test", title='title for test')
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.content_id = content.id

    def test_create_rating(self):
        payload = {
            'score': 5
        }
        response = self.client.post(f'/content/{self.content_id}/rating/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_rating(self):
        existing_rating = Rating.objects.create(user=self.user, content_id=self.content_id, score=3)
        payload = {
            'score': 4
        }
        response = self.client.put(f'/content/{self.content_id}/rating/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)