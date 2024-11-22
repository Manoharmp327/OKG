from django.db import models
from ckeditor.fields import RichTextField

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Subtitle(models.Model):
    course = models.ForeignKey(Course, related_name='subtitles', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.course.title} - {self.name}"

class Video(models.Model):
    subtitle = models.ForeignKey(Subtitle, related_name='videos', on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class PDF(models.Model):
    subtitle = models.ForeignKey(Subtitle, related_name='pdfs', on_delete=models.CASCADE)
    file = models.FileField(upload_to='pdfs/')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Notes(models.Model):
    subtitle = models.ForeignKey(Subtitle, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Untitled')
    content = RichTextField()

    def __str__(self):
        return f"Notes for {self.subtitle.name} - {self.title}"
