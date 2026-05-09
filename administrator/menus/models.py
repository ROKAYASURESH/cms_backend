from django.db import models
from django.utils.text import slugify

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    url = models.CharField(max_length=255, blank=True)
    icon = models.TextField(default='fa fa-th-list', null=True, blank=True)
    position = models.IntegerField(blank=True, null=True)
    publish = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.position is None:
            last_position = Menu.objects.aggregate(max_position=models.Max('position'))['max_position']
            self.position = 1 if last_position is None else last_position + 1
        
        if not self.slug:
            self.slug = slugify(self.title)
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return self.title