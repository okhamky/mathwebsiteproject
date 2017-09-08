from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
            ordering = ["last_name"]

    def __str__(self):
        return self.first_name + self.last_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ManyToManyField(Teacher)

    class Meta:
            ordering = ["user__last_name"]

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Book(models.Model):
    book_name = models.CharField(max_length=100)

    def __str__(self):
        return self.book_name + "Book Object"


class Chapter(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    chapter_weight = models.FloatField(default=1)

    def in_book(self):
        return self.book

    def __str__(self):
        return self.book.book_name + " - " + str(self.chapter_number) + "Chapter Object"


class PaceChapter(models.Model):
    #add limited lists
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    is_review = models.BooleanField(default=False)
    pace_date = models.DateField(blank=True, null=True)
    complete_date = models.DateField(blank=True, null=True)
    attempts = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    class Meta:
        #add secondary ordering
        ordering = ['pace_date']

    def __str__(self):
        return str(self.chapter) + "Pace Chapter Object"
