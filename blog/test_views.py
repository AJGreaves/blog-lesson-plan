from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test", password="test", email="test@test.com")
        self.post = Post(title="Test post", author=self.user, slug="test",
                         excerpt="Test excerpt", content="Test content", status=1)
        self.post.save()

    def test_get_post_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_get_post(self):
        response = self.client.get(reverse('post_detail', args=['test']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_display_post_details(self):
        response = self.client.get(reverse('post_detail', args=['test']))
        self.assertIn(b"Test post", response.content)
        self.assertIn(b"Test content", response.content)

    def test_comment_submission(self):
        self.client.login(username="test", password="test")
        response = self.client.post(reverse('post_detail', args=['test']), {
            'body': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comment submitted and awaiting approval',
                      response.content)
        self.assertTrue(Comment.objects.filter(
            body="This is a test comment.").exists())

    def test_nonexistent_post(self):
        response = self.client.get(
            reverse('post_detail', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
