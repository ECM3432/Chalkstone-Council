from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from issues.models import Issue
from comments.models import Comment  # Assuming your Comment model is here

User = get_user_model()

class AddCommentViewTest(TestCase):
    def setUp(self):
        # Create a test user.
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        # Create a test issue.
        self.issue = Issue.objects.create(
            title="Test Issue",
            status="Open",
            category="Pothole",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        # Build URL for adding a comment (assumes URL name is 'add_comment')
        self.url = reverse('add_comment', kwargs={'issue_id': self.issue.id})

    def test_add_comment_requires_login(self):
        """
        A non-logged in user should be redirected to the login page.
        """
        response = self.client.post(self.url, data={'text': 'Test comment'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_add_comment_valid_post(self):
        """
        A logged-in user can post a valid comment.
        The view should create a Comment and redirect to the issue detail page.
        """
        self.client.login(username='testuser', password='testpass')
        initial_count = Comment.objects.count()
        data = {'text': 'Test comment from logged-in user'}
        response = self.client.post(self.url, data=data)
        # Check for a redirect response.
        self.assertEqual(response.status_code, 302)
        expected_redirect = reverse('issue_detail', kwargs={'pk': self.issue.id})
        self.assertEqual(response.url, expected_redirect)
        # Verify that a new Comment was created.
        self.assertEqual(Comment.objects.count(), initial_count + 1)
        comment = Comment.objects.latest('id')
        self.assertEqual(comment.text, data['text'])
        self.assertEqual(comment.issue, self.issue)
        self.assertEqual(comment.author, self.user)

    def test_add_comment_invalid_post(self):
        """
        Posting invalid data (e.g. missing 'text') should not create a Comment.
        The view will still redirect to the issue detail page.
        """
        self.client.login(username='testuser', password='testpass')
        initial_count = Comment.objects.count()
        # Sending empty data; assuming the form requires 'text'.
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), initial_count)
