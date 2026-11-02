from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        'onlinecourseapp/course_details_bootstrap.html',
        {'course': course}
    )


@login_required
def submit(request, lesson_id):
    lesson_questions = Question.objects.filter(lesson_id=lesson_id)

    if request.method == 'POST':
        for question in lesson_questions:
            selected_choice_id = request.POST.get(str(question.id))

            if selected_choice_id:
                selected_choice = get_object_or_404(
                    Choice,
                    id=selected_choice_id,
                    question=question
                )

                Submission.objects.update_or_create(
                    student=request.user,
                    question=question,
                    defaults={
                        'selected_choice': selected_choice,
                        'is_correct': selected_choice.is_correct
                    }
                )

        return redirect('show_exam_result', lesson_id=lesson_id)

    return render(
        request,
        'onlinecourseapp/exam.html',
        {'questions': lesson_questions, 'lesson_id': lesson_id}
    )


@login_required
def show_exam_result(request, lesson_id):
    questions = Question.objects.filter(lesson_id=lesson_id)

    submissions = Submission.objects.filter(
        student=request.user,
        question__in=questions
    ).select_related('question', 'selected_choice')

    total_questions = questions.count()
    correct_answers = submissions.filter(is_correct=True).count()

    score = (
        round((correct_answers / total_questions) * 100)
        if total_questions else 0
    )

    return render(
        request,
        'onlinecourseapp/exam_result.html',
        {
            'questions': questions,
            'submissions': submissions,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score,
        }
    )