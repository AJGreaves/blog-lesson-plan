from .models import Post
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm


class TestBlogViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test", password="test", email="test@test.com")
        self.post = Post(title="Test post", author=self.user, slug="test-post",
                         excerpt="Test excerpt", content="Test content", status=1)
        self.post.save()

    def test_render_post_detail_page_with_comment_form(self):
        response = self.client.get(reverse('post_detail', args=['test-post']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test post", response.content)
        self.assertIn(b"Test content", response.content)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

    # def test_successful_comment_submission(self):
    #     self.client.login(username="test", password="test")
    #     post_data = {
    #         'body': 'This is a test comment.'
    #     }
    #     response = self.client.post(
    #         reverse('post_detail', args=['test']), post_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Comment submitted and awaiting approval',
    #                   response.content)
