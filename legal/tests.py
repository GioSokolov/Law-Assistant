from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from legal.models import Law, Code, InterpretationDecision, Article, ArticleComment, ArticleLike
import datetime


class LegalTests(TestCase):
    def setUp(self):
        # Създаване на тестови данни
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Създаване на тестов закон
        self.law = Law.objects.create(
            title="Test Law",
            content="This is a test law content.",
            published_date=datetime.date.today(),
        )

        # Създаване на тестов кодекс
        self.code = Code.objects.create(
            title="Test Code",
            content="This is a test code content.",
            published_date=datetime.date.today(),
        )

        # Създаване на тестово тълкувателно решение
        self.interpretation = InterpretationDecision.objects.create(
            title="Test Interpretation",
            content="This is a test interpretation content.",
            published_date=datetime.date.today(),
            category="labor"
        )

        # Създаване на тестова статия
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            slug="test-article",
            author=self.user  # Задаване на автора
        )

    def test_laws_list(self):
        response = self.client.get(reverse('laws_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.law.title)

    def test_codes_list(self):
        response = self.client.get(reverse('codes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.code.title)

    def test_interpretations_list(self):
        response = self.client.get(reverse('interpretations_list', kwargs={'category': 'labor'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.interpretation.title)

    def test_add_comment(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('add_comment', kwargs={'slug': self.article.slug}), {
            'content': "This is a test comment."
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ArticleComment.objects.filter(content="This is a test comment.").exists())

    def test_toggle_like(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('toggle_like', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ArticleLike.objects.filter(article=self.article, user=self.user).exists())

        response = self.client.post(reverse('toggle_like', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ArticleLike.objects.filter(article=self.article, user=self.user).exists())
