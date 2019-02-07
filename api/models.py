from django.db import models

class DemoEntries(models.Model):

    text = models.TextField()
    save_time = models.DateTimeField(auto_now_add=True)