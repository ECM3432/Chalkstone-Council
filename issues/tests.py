# tests_minimal.py
from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Issue
from .forms import UserIssueForm, StaffIssueForm
from comments.forms import CommentForm
from .views import issue_category

User = get_user_model()

@override_settings(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                (
                    'django.template.loaders.locmem.Loader',
                    {
                        'issues/issue_list.html': 'dummy issue_list',
                        'issues/issue_detail.html': 'dummy issue_detail',
                        'issues/issue_form.html': 'dummy issue_form',
                        'issues/issue_edit.html': 'dummy issue_edit',
                        'issues/issue_confirm_delete.html': 'dummy issue_confirm_delete',
                        'issues/issue_category_list.html': 'dummy issue_category_list',
                    }
                ),
            ],
        },
    }]
)
class MinimalValidTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a valid set of category choices.
        Issue.CATEGORY_CHOICES = [
            ('Bug', 'Bug'),
            ('Feature', 'Feature'),
            ('Task', 'Task'),
        ]
        # Create one staff user and one regular user.
        cls.staff_user = User.objects.create_user(username='staff', password='password', is_staff=True)
        cls.regular_user = User.objects.create_user(username='regular', password='password', is_staff=False)
        # Create a few issues.
        cls.issue1 = Issue.objects.create(
            title="Issue 1",
            description="Description 1",
            category="Bug",
            reporter=cls.regular_user,
            status="Open"
        )
        cls.issue2 = Issue.objects.create(
            title="Issue 2",
            description="Description 2",
            category="Feature",
            reporter=cls.staff_user,
            status="Open"
        )
        # A closed issue should be excluded from the list view.
        cls.closed_issue = Issue.objects.create(
            title="Closed Issue",
            description="Closed description",
            category="Task",
            reporter=cls.regular_user,
            status="Closed"
        )
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
    
    # --- issue_list view ---
    def test_issue_list_authenticated_staff(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('issue_list'))
        self.assertEqual(response.status_code, 200)
        issues = response.context['issues']
        self.assertIn(self.issue1, issues)
        self.assertIn(self.issue2, issues)
        self.assertNotIn(self.closed_issue, issues)
        self.assertTrue(response.context['users'])
    
    def test_issue_list_authenticated_regular(self):
        self.client.login(username='regular', password='password')
        response = self.client.get(reverse('issue_list'))
        self.assertEqual(response.status_code, 200)
        issues = response.context['issues']
        self.assertIn(self.issue1, issues)
        self.assertIn(self.issue2, issues)
        self.assertNotIn(self.closed_issue, issues)
        self.assertEqual(response.context['users'], [])
    
    def test_issue_list_unauthenticated(self):
        response = self.client.get(reverse('issue_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['issues'])
        self.assertEqual(response.context['users'], [])
    
    # --- issue_detail view ---
    def test_issue_detail(self):
        url = reverse('issue_detail', args=[self.issue1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['issue'], self.issue1)
        self.assertIsInstance(response.context['comment_form'], CommentForm)
    
    # --- issue_create view ---
    def test_issue_create_get_regular(self):
        self.client.login(username='regular', password='password')
        response = self.client.get(reverse('issue_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserIssueForm)
    
    def test_issue_edit_regular(self):
        self.client.login(username='regular', password='password')
        url = reverse('issue_edit', args=[self.issue1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserIssueForm)
        data = {'title': 'Edited Issue 1', 'description': 'Edited desc', 'category': 'Bug'}
        response = self.client.post(url, data)
        self.issue1.refresh_from_db()
        self.assertEqual(self.issue1.title, 'Issue 1')
    
    def test_issue_edit_staff(self):
        self.client.login(username='staff', password='password')
        url = reverse('issue_edit', args=[self.issue2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], StaffIssueForm)
        data = {'title': 'Edited Issue 2', 'description': 'Edited desc 2', 'category': 'Feature', 'status': 'Open'}
        response = self.client.post(url, data)
        self.issue2.refresh_from_db()
        self.assertEqual(self.issue2.title, 'Issue 2')
    
    # --- issue_delete view (staff only) ---
    def test_issue_delete_staff(self):
        self.client.login(username='staff', password='password')
        url = reverse('issue_delete', args=[self.issue1.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Issue.DoesNotExist):
            Issue.objects.get(pk=self.issue1.pk)
    
    # --- issue_category view ---
    def test_issue_category(self):
        self.client.login(username='regular', password='password')
        url = reverse('issue_category', kwargs={'category': 'Bug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('issues', response.context)
        self.assertIn('categories', response.context)
