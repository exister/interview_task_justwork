from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.models import PolymorphicModel


class Page(models.Model):
    title = models.CharField(max_length=255)
    content = models.ManyToManyField("Content", through="PageContent")

    def __str__(self):
        return self.title


class Content(PolymorphicModel):
    title = models.CharField(max_length=255)
    counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Video(Content):
    video_file_url = models.URLField()
    subtitles_file_url = models.URLField()


class Audio(Content):
    audio_file_url = models.URLField()
    bitrate = models.PositiveSmallIntegerField()


class Text(Content):
    content = models.TextField()


class PageContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ("order",)
        unique_together = (("page", "content"),)

    def __str__(self):
        return f"{self.content.polymorphic_ctype} {self.content.title}"
