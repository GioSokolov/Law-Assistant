from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Law(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="laws"  # Пример: laws
    )
    document = models.FileField(upload_to="laws/", blank=True, null=True)

    def __str__(self):
        return self.title


class Code(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="codes"  # Пример: codes
    )
    document = models.FileField(upload_to="codes/", blank=True, null=True)

    def __str__(self):
        return self.title


class InterpretationDecision(models.Model):
    CATEGORY_CHOICES = [
        ('labor', 'Трудови'),
        ('family', 'Семейни'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    published_date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    document = models.FileField(upload_to='interpretations/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class DocumentFile(models.Model):
    document = models.ForeignKey(Law, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="documents/")

    def __str__(self):
        return f"File for {self.document.title}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(blank=True, null=True)  # Съдържанието може да е опционално, ако качвате PDF.
    published_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    document = models.FileField(upload_to='articles/documents/', blank=True, null=True)  # Поле за PDF документ.

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user} likes {self.article}"
