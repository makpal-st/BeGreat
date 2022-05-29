from django.urls import path, include

from course.views import CourseViewSet, CourseSurveyViewSet, CourseLecturesViewSet, LectureNoteViewSet, MultitestViewSet

urlpatterns = [
    path(
        '',
        CourseViewSet.as_view({'get': 'list_courses'}),
        name='get courses'
    ),
    path(
        '<int:course_id>/categories/',
        CourseViewSet.as_view({'get': 'list_categories'}),
        name='get course categories'
    ),
    path(
        'join/',
        CourseViewSet.as_view({'post': 'join_course'}),
        name='join_course'
    ),
    path(
        '<int:category_id>/questionaire/',
        CourseSurveyViewSet.as_view({'get': 'questions'}),
        name='survey'
    ),
    path(
        '<int:category_id>/submit/',
        CourseSurveyViewSet.as_view({'post': 'submit_answer'}),
        name='submit answer'
    ),
    path(
        '<int:category_id>/lectures/',
        CourseLecturesViewSet.as_view({'get': 'lecture_materials'}),
        name='lectures'
    ),
    path(
        '<int:category_id>/post_note/',
        LectureNoteViewSet.as_view({'post': 'post_note'}),
        name='post_note'
    ),
    path(
        'multitests/generate/',
        MultitestViewSet.as_view({'post': 'generate'}),
        name='generate_multitest'
    ),
    path(
        'multitest/get_questions/',
        MultitestViewSet.as_view({'get': 'get_questions'}),
        name='get multitest questions'
    ),
    path(
        'multitest/answer/<category_id>/',
        MultitestViewSet.as_view({'post': 'submit_answer'}),
        name='answer to multitest'
    ),
    path(
        'multitest/result/',
        MultitestViewSet.as_view({'get': 'get_result'}),
        name='get result of multitest'
    )
]
