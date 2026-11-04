from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Lesson, Enrollment


class Question(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='questions',
        null=True,
        blank=True
    )
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        correct_ids = set(
            self.choices.filter(is_correct=True)
            .values_list('id', flat=True)
        )
        selected_ids = {int(choice_id) for choice_id in selected_ids}
        return correct_ids == selected_ids

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='submissions',
        null=True,
        blank=True
    )
    choices = models.ManyToManyField(
        Choice,
        related_name='submissions',
        blank=True
    )

    # Retained for compatibility with existing records and code.
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True
    )
    selected_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True
    )
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.enrollment:
            return f"Submission: {self.enrollment}"
        return f"Submission {self.pk}"
