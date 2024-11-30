from django.db import models


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
