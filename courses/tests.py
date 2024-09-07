from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

from courses.models import Course, Lesson
from courses.validators import ValidateOnlyYoutubeLink
from courses.regexp import check_youtube_string


# ===============================CourseTests===============================
class TestCourseAPI(APITestCase):
    """Тесты курса
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test',
            email='test@gmail.com',
            password='testroot',
            )
        self.client.force_authenticate(user=self.user)
        self.course_url = 'http://127.0.0.1:8000/api/course/'

    def test_view_course(self):
        """Тест вывода курса
        """
        course = Course.objects.create(
            owner=self.user,
            course_name='course',
            description='description_of_the_course',
            )
        url = self.course_url + str(course.pk) + '/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'pk': course.pk,
            'course_name': 'course',
            'course_preview': None,
            'description': 'description_of_the_course',
            'subscribe_of_the_course': False,
            'lessons': 0,
            'lessons_detail': [],
            })

    def test_view_list_courses(self):
        """Тест списка из курсов
        """
        Course.objects.create(
            owner=self.user,
            course_name='course_first',
            description='description_of_the_course_first',
            )
        Course.objects.create(
            owner=self.user,
            course_name='course_second',
            description='description_of_the_course_second',
            )
        url = self.course_url

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data['count'], 2)

    def test_create_course(self):
        """Тест создания курса
        """
        url = self.course_url
        data = {'owner': self.user.pk,
                'course_name': 'course',
                'description': 'description_of_the_course'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().description,
                         'description_of_the_course',
                         )

    def test_update_course(self):
        """Тест обновления курса
        """
        course = Course.objects.create(
            owner=self.user,
            course_name='course',
            description='description_of_the_course',
            )
        url = self.course_url + str(course.pk) + '/'
        data = {'description': 'update_description'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get().description,
                         'update_description',
                         )

    def test_count_lessons_into_course(self):
        """Тест количества уроков у курса
        """
        course = Course.objects.create(
            owner=self.user,
            course_name='course',
            description='description_of_the_course',
            )

        url_lesson = reverse('courses:lesson_list')
        url_course = self.course_url + str(course.pk) + '/'
        data = {
            'owner': self.user.pk,
            'course': course.pk,
            'lesson_name': 'lesson',
            'description': 'description_of_the_lesson',
            'video_link': 'https://www.youtube.com/some-video/'
        }
        self.client.post(url_lesson, data, format='json')
        self.client.post(url_lesson, data, format='json')
        self.client.post(url_lesson, data, format='json')
        self.client.post(url_lesson, data, format='json')
        response = self.client.get(url_course)

        self.assertEqual(response.data['lessons'], 4)

    def test_delete_course(self):
        """Тест удаления курса
        """
        course = Course.objects.create(
            owner=self.user,
            course_name='course',
            description='description_of_the_course',
            )
        url = self.course_url + str(course.pk) + '/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(
            course_name='course',
            ).exists())
        self.assertEqual(Course.objects.count(), 0)


# ===============================LessonTests===============================
class TestLessonAPI(APITestCase):
    """Тесты уроков
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test',
            email='test@gmail.com',
            password='testroot',
            )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            owner=self.user,
            course_name='course',
            description='description_of_the_course',
            )

    def test_view_lesson(self):
        """Тест вывода урока
        """
        lesson = Lesson.objects.create(
            owner=self.user,
            course=self.course,
            lesson_name='lesson',
            description='description_of_the_lesson',
            video_link='https://www.youtube.com/some-video/',
            )
        url = reverse('courses:lesson_detail', kwargs={'pk': lesson.pk})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'pk': lesson.pk,
            'course': self.course.pk,
            'lesson_name': 'lesson',
            'description': 'description_of_the_lesson',
            'lesson_preview': None,
            'video_link': 'https://www.youtube.com/some-video/',
            })

    def test_view_list_lessons(self):
        """Тест вывода списка из уроков
        """
        Lesson.objects.create(
            owner=self.user,
            course=self.course,
            lesson_name='lesson_first',
            description='description_of_the_lesson_first',
            video_link='https://www.youtube.com/some-video/1/',
            )
        Lesson.objects.create(
            owner=self.user,
            course=self.course,
            lesson_name='lesson_second',
            description='description_of_the_lesson_second',
            video_link='https://www.youtube.com/some-video/2/',
            )

        url = reverse('courses:lesson_list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(response.data['count'], 2)

    def test_create_lesson(self):
        """Тест создания урока
        """
        url = reverse('courses:lesson_list')
        data = {
            'owner': self.user.pk,
            'course': self.course.pk,
            'lesson_name': 'lesson',
            'description': 'description_of_the_lesson',
            'video_link': 'https://www.youtube.com/some-video/'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(
            lesson_name='lesson',
            ).exists())
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_common_link_video_lesson(self):
        """Тест создания урока с обычным адрессом ссылки видео
        """
        url = reverse('courses:lesson_list')
        data = {
            'owner': self.user.pk,
            'course': self.course.pk,
            'lesson_name': 'lesson',
            'description': 'description_of_the_lesson',
            'video_link': 'path/to/some/video'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(
            video_link='path/to/some/video',
            ).exists())
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_bad_link_video_lesson(self):
        """Тест не подходящей ссылки видео в уроке
        """
        url = reverse('courses:lesson_list')
        data = {
            'owner': self.user.pk,
            'course': self.course.pk,
            'lesson_name': 'lesson',
            'description': 'description_of_the_lesson',
            'video_link': 'https://www.bad_video.com/some-video/'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson(self):
        """Тест обновления урока
        """
        lesson = Lesson.objects.create(
            owner=self.user,
            course=self.course,
            lesson_name='lesson',
            description='description_of_the_lesson',
            video_link='https://www.youtube.com/some-video/',
            )
        data = {
            'description': 'update_description'
        }
        url = reverse('courses:lesson_detail', kwargs={'pk': lesson.pk})

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.filter(
            description='update_description',
            ).exists())
        self.assertFalse(Lesson.objects.filter(
            description='description_of_the_lesson',
            ).exists())

    def test_delete_lesson(self):
        """Тест удаления урока
        """
        lesson = Lesson.objects.create(
            owner=self.user,
            course=self.course,
            lesson_name='lesson',
            description='description_of_the_lesson',
            video_link='https://www.youtube.com/some-video/',
            )
        url = reverse('courses:lesson_detail', kwargs={'pk': lesson.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_validate_only_youtube_link(self):
        """Проверка валидатора на тип данных
        """
        validate = ValidateOnlyYoutubeLink(link='link')

        self.assertEqual(validate.link, 'link')
        self.assertIsNone(validate(attrs={'link': 'https://youtube/'}))
        with self.assertRaises(TypeError):
            ValidateOnlyYoutubeLink(['srt'])

    def test_youtube_string(self):
        """Тест регулярного выражения для проверки ютуб строки
        """
        self.assertIsNone(check_youtube_string(1223))
        self.assertIsNone(check_youtube_string('some_bad_site'))
        self.assertIsNone(check_youtube_string('www.some_bad_site.com'))
        self.assertTrue(bool(check_youtube_string('youtube')))
        self.assertTrue(bool(check_youtube_string('www.youtube.com')))
        self.assertTrue(bool(check_youtube_string('youtu.be')))


# ===============================SubscribeTests===============================
class TestSubscribeAPI(APITestCase):
    """Тесты подписок
    """

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username='test',
            email='test@gmail.com',
            password='testroot',
            )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            owner=self.user,
            course_name='course',
            description='description_of_the_course',
            )
        self.course_url = 'http://127.0.0.1:8000/api/course/'

    def test_set_subscribe(self):
        """Тест подписки на курс
        """
        url_subscribe = reverse(
            'courses:subscribe',
            kwargs={'pk': self.course.pk},
            )
        url_course = self.course_url + str(self.course.pk) + '/'
        response_subscribe = self.client.post(url_subscribe)
        response_course = self.client.get(url_course)

        self.assertEqual(response_subscribe.status_code, status.HTTP_200_OK)
        self.assertTrue(response_course.data['subscribe_of_the_course'])

    def test_unsubscribe(self):
        """Тест отписки от курса
        """
        url_subscribe = reverse(
            'courses:subscribe',
            kwargs={'pk': self.course.pk},
            )
        url_course = self.course_url + str(self.course.pk) + '/'
        self.client.post(url_subscribe)
        self.client.post(url_subscribe)
        response_course = self.client.get(url_course)

        self.assertFalse(response_course.data['subscribe_of_the_course'])
