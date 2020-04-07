import datetime
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 100) # Title limit set to 150 characters.
    slug = models.SlugField(unique = True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add = True) # Automatically populate this with date and time at the time of posting.
    updated = models.DateTimeField(auto_now = True) # To be updated when we edit the posts.
    author = models.ForeignKey(User, default = None, on_delete=models.DO_NOTHING,)

    def __str__(self):
        return self.title

    def snippet(self):
        bodyText = self.body
        if len(bodyText) > 400:
            return bodyText[:400] + "..." # Snippet of 400 characters to be displayed at home-page of the blog.
        else:
            return bodyText

    def isUpdated(self):
        dateEdit = self.updated
        datePublished = self.date
        difference = dateEdit - datePublished
        diffInSeconds = difference.days*24*3600 + difference.seconds
        return (diffInSeconds > 60)

    def save(self, *args, **kwargs): # overriding the save method. SlugField is automatically populated as we enter the title.
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(self.author)+'-'+str(datetime.date.today()))
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date", "-updated"] # Specifies the order in which the posts are displayed, latest first.
