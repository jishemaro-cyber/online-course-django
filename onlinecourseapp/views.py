from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from courses.models import Course, Lesson, Enrollment
from .models import Question, Choice, Submission
from courses.models import Learner


def home(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourseapp/home.html', {
        'courses': courses
    })


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        'onlinecourseapp/course_details_bootstrap.html',
        {'course': course}
    )


@login_required
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(course=course).prefetch_related('choices')

    if request.method == 'POST':
        learner, _ = Learner.objects.get_or_create(user=request.user)
        enrollment, _ = Enrollment.objects.get_or_create(
            learner=learner,
            course=course
        )

        submission = Submission.objects.create(enrollment=enrollment)
        selected_choices = []

        for question in questions:
            selected_id = request.POST.get(str(question.id))
            if selected_id:
                choice = get_object_or_404(
                    Choice,
                    id=selected_id,
                    question=question
                )
                selected_choices.append(choice)

        submission.choices.set(selected_choices)
        return redirect(
            'show_exam_result',
            course_id=course.id,
            submission_id=submission.id
        )

    return render(request, 'onlinecourseapp/exam.html', {
        'course': course,
        'questions': questions,
    })


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(
        Submission.objects.select_related('enrollment__learner__user'),
        id=submission_id,
        enrollment__course=course,
        enrollment__learner__user=request.user
    )

    selected_choices = list(submission.choices.select_related('question'))
    selected_ids = [choice.id for choice in selected_choices]

    questions = Question.objects.filter(course=course).prefetch_related('choices')
    grade = 0
    total_points = sum(question.grade for question in questions)

    for question in questions:
        question_selected_ids = [
            choice.id for choice in selected_choices
            if choice.question_id == question.id
        ]
        if question.is_get_score(question_selected_ids):
            grade += question.grade

    percentage = round((grade / total_points) * 100) if total_points else 0

    return render(
        request,
        'onlinecourseapp/exam_result_bootstrap.html',
        {
            'course': course,
            'submission': submission,
            'selected_ids': selected_ids,
            'grade': grade,
            'total_points': total_points,
            'percentage': percentage,
            'questions': questions,
            'selected_choices': selected_choices,
        }
    )
