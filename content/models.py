from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=45, unique=True)
    pr_1 = models.TextField()
    pr_2 = models.TextField()
    pr_3 = models.TextField()
    img_1 = models.TextField()
    img_2 = models.TextField()
    img_3 = models.TextField()