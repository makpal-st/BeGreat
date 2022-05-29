from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from achievement.models import UserAchievement, Achievement
from course.models import UserCourse, QuestionAnswer, QuestionOption, Question, Lecture, MultiTest
from utils import constants


def can_user_join_course(user, category_id, anonymous_user):
    if not user:
        if UserCourse.objects.filter(anonymous_user=anonymous_user).exists():
            raise ValidationError('Вы уже взяли пробный урок!')
        qs = UserCourse.objects.filter(anonymous_user=anonymous_user, category_id=category_id).first()
    else:
        qs = UserCourse.objects.filter(user_id=user.id, category_id=category_id).first()
    if qs:
        raise ValidationError('Вы уже брали этот курс')


def join_course(user, category_id, anonymous_user=None):
    user_course = UserCourse.objects.create(user=user, category_id=category_id, anonymous_user=anonymous_user)
    return user_course


def get_user_course(user, anonymous_user, category_id):
    if user.is_authenticated:
        return UserCourse.objects.filter(user_id=user.id, category_id=category_id).first()
    return UserCourse.objects.filter(anonymous_user=anonymous_user, category_id=category_id).first()


def save_note(user, category_id, note, anonymous_user):
    user_course = get_user_course(user, anonymous_user, category_id)
    if not user_course.note:
        user_course.note = note
    else:
        user_course.note += "\n" + note
    user_course.save()


def check_answer(user, question, answer_option, answer_type, multitest=None):
    try_counter = QuestionAnswer.objects.filter(user=user, question_id=question).count() + 1
    kwargs = {
        "user": user,
        "question_id": question,
        "option_id": answer_option,
        "attempt_counter": try_counter,
        "type": answer_type,
    }
    question = Question.objects.get(id=question)
    if answer_type == QuestionAnswer.MULTITEST and multitest:
        kwargs["multitest_id"] = multitest.id
    else:
        answers_count = QuestionAnswer.objects.filter(user_id=user.id, question__category_id=question.category_id, option__value=1).distinct('question').count()
        questions_count = Question.objects.filter(category_id=question.category_id).count()
        if answers_count == questions_count:
            user_course = UserCourse.objects.filter(
                is_finished=False, category_id=question.category_id, user_id=user.id
            ).first()
            if user_course:
                user_course.is_finished = True
                user_course.save(update_fields=('is_finished',))
            else:
                ValidationError('Вы не проходите этот курс!')
    QuestionAnswer.objects.create(**kwargs)
    if multitest:
        answers = QuestionAnswer.objects.filter(
            multitest_id=multitest.id,
            option__value=1
        ).distinct('question')
        if answers.count() == multitest.question.all().count():
            multitest.is_finished = True
        result = 0
        checked = []
        for x in answers:
            if x.id not in checked and x.option.value:
                checked.append(x.id)
                result += x.option.value
        multitest.result = result
        multitest.save(update_fields=('result', 'is_finished'))
    result = QuestionOption.objects.get(id=answer_option)
    if result.value:
        return {'result': constants.CORRECT, 'text': constants.CORRECT_ANSWER_TEXT}
    return {'result': constants.WRONG, 'text': constants.WRONG_ANSWER_TEXT}


def get_finished_courses(user):
    return UserCourse.objects.filter(is_finished=True, user_id=user.id)


def get_answered_question_number(user_course: UserCourse):
    result = QuestionAnswer.objects.filter(
        user_id=user_course.user, question__category_id=user_course.category_id, option__value=1
    ).distinct('question_id').count() / Question.objects.filter(
        category_id=user_course.category_id
    ).count()
    return int(result * 100)


def add_passed_lectures(user, lectures):
    lectures = [x.id for x in lectures]
    user.account.passed_lectures += lectures
    user.account.save(update_fields=('passed_lectures',))


def generate_multitest(user):
    if MultiTest.objects.filter(user_id=user.id, result=0).first():
        raise ValidationError('У вас имеется незавершенный мультитест!')
    lectures = Lecture.objects.filter(id__in=user.account.passed_lectures)
    categories = lectures.values_list('category_id', flat=True)
    questions = Question.objects.filter(category_id__in=categories).order_by('?')[:10]
    multi_test = MultiTest.objects.create(user=user)
    for q in questions:
        multi_test.question.add(q)


def get_result_of_multitest(user):
    multitest = MultiTest.objects.filter(user_id=user.id, is_finished=True).first()
    if multitest and \
            QuestionAnswer.objects.filter(multitest_id=multitest.id).distinct('question').count() >= multitest.question.all().count():
        achievement = Achievement.objects.filter(min_points__lte=multitest.result).order_by('-min_points').first()
        if not UserAchievement.objects.filter(multitest_id=multitest.id, achievement_id=achievement.id).first():
            UserAchievement.objects.create(user_id=user.id, achievement_id=achievement.id)
    user_achievements = UserAchievement.objects.filter(user_id=user.id)
    return user_achievements
