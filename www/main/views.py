from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import (
    User, Author, Book, PlatformStatistics, HeroBlock, StudentBlock, TeacherBlock,
    Screenshot, Testimonial, PricingPlan, Lead, Course
)
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    AuthorSerializer, BookSerializer,
    PlatformStatisticsSerializer, HeroBlockSerializer, StudentBlockSerializer,
    TeacherBlockSerializer, ScreenshotSerializer, TestimonialSerializer,
    PricingPlanSerializer, LeadSerializer, CourseSerializer
)
from .permissions import IsAdminOrContentManager, IsOwnerOrReadOnly
from .pagination import StandardResultsSetPagination, SmallResultsSetPagination
from .filters import BookFilter, LeadFilter

from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Согласно ТЗ: создание пользователей (студентов/преподавателей)
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Вход пользователя.
    Возвращает JWT токены для доступа к API.
    Согласно ТЗ: JWT-аутентификация для ролевой модели управления.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============= ПОЛЬЗОВАТЕЛИ =============

class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями.
    GET /api/users/ - список пользователей (только админ)
    POST /api/users/ - регистрация (доступно всем)
    GET /api/users/me/ - текущий пользователь (требует аутентификации)

    Согласно ТЗ: ролевая модель управления (студенты, преподаватели, контент-менеджеры)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'date_joined']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Получить информацию о текущем пользователе"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# ============= АВТОРЫ =============

class AuthorViewSet(viewsets.ModelViewSet):
    """
    Управление авторами книг.
    Пример работы с Foreign Key для демонстрации связей в API.

    Согласно ТЗ: пример работы со связанными данными
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


# ============= КНИГИ =============

class BookViewSet(viewsets.ModelViewSet):
    """
    Управление книгами.
    Полный CRUD для демонстрации работы с API.
    Включает фильтрацию, поиск, сортировку и пагинацию.

    Согласно ТЗ: пример работы с динамическими данными через API
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['price', 'pages', 'published_date', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


# ============= СТАТИСТИКА ПЛАТФОРМЫ =============

class PlatformStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Статистика платформы.
    GET /api/statistics/ - возвращает актуальную статистику.

    Согласно ТЗ пункт 3.2: вывод актуальной статистики платформы
    (количество активных курсов, студентов)
    """
    queryset = PlatformStatistics.objects.all()
    serializer_class = PlatformStatisticsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Возвращаем только последнюю запись статистики
        return PlatformStatistics.objects.order_by('-updated_at')[:1]


# ============= HERO БЛОК =============

class HeroBlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Hero блок лендинга.
    GET /api/hero/ - возвращает активный hero-блок.

    Согласно ТЗ пункт 3.2: динамический контент лендинга
    """
    queryset = HeroBlock.objects.filter(is_active=True)
    serializer_class = HeroBlockSerializer
    permission_classes = [permissions.AllowAny]


# ============= БЛОКИ ДЛЯ СТУДЕНТОВ =============

class StudentBlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Блоки "Для студентов".
    GET /api/student-blocks/ - возвращает активные блоки.

    Согласно ТЗ пункт 3.2: презентация функционала прохождения курсов,
    тестирования и механизма соревновательных дуэлей
    """
    queryset = StudentBlock.objects.filter(is_active=True)
    serializer_class = StudentBlockSerializer
    permission_classes = [permissions.AllowAny]


# ============= БЛОКИ ДЛЯ ПРЕПОДАВАТЕЛЕЙ =============

class TeacherBlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Блоки "Для преподавателей".
    GET /api/teacher-blocks/ - возвращает активные блоки.

    Согласно ТЗ пункт 3.2: демонстрация конструктора уроков
    и графиков аналитики успеваемости
    """
    queryset = TeacherBlock.objects.filter(is_active=True)
    serializer_class = TeacherBlockSerializer
    permission_classes = [permissions.AllowAny]


# ============= СКРИНШОТЫ =============

class TestimonialViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов"""
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

    def get_permissions(self):
        """GET доступен всем, остальное - только админам"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ScreenshotViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для скриншотов"""
    queryset = Screenshot.objects.filter(is_active=True)
    serializer_class = ScreenshotSerializer
    permission_classes = [AllowAny]
# ============= ТАРИФЫ =============

class PricingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Тарифные планы.
    GET /api/pricing/ - возвращает активные тарифы.

    Согласно ТЗ пункт 3.2: секция тарифов
    """
    queryset = PricingPlan.objects.filter(is_active=True)
    serializer_class = PricingPlanSerializer
    permission_classes = [permissions.AllowAny]


# ============= ОБЪЕДИНЕННЫЙ ЭНДПОИНТ ДЛЯ ЛЕНДИНГА =============

class LandingPageAPIView(APIView):
    """
    Объединенный эндпоинт для всех данных лендинга.
    GET /api/landing/ - возвращает все данные для одной страницы.

    Согласно ТЗ:
    - Снижение количества запросов от фронтенда
    - Динамическое управление контентом через административную панель
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Собираем все данные для лендинга в одном ответе.
        """
        data = {
            # Hero блок
            'hero': HeroBlockSerializer(
                HeroBlock.objects.filter(is_active=True).first()
            ).data if HeroBlock.objects.filter(is_active=True).exists() else None,

            # Блоки для студентов
            'student_blocks': StudentBlockSerializer(
                StudentBlock.objects.filter(is_active=True),
                many=True
            ).data,

            # Блоки для преподавателей
            'teacher_blocks': TeacherBlockSerializer(
                TeacherBlock.objects.filter(is_active=True),
                many=True
            ).data,

            # Статистика платформы
            'statistics': PlatformStatisticsSerializer(
                PlatformStatistics.objects.order_by('-updated_at').first()
            ).data if PlatformStatistics.objects.exists() else None,

            # Скриншоты (раздельно для студентов и преподавателей)
            'screenshots': {
                'student': ScreenshotSerializer(
                    Screenshot.objects.filter(is_active=True, section='student'),
                    many=True
                ).data,
                'teacher': ScreenshotSerializer(
                    Screenshot.objects.filter(is_active=True, section='teacher'),
                    many=True
                ).data,
            },

            # Отзывы
            'testimonials': TestimonialSerializer(
                Testimonial.objects.filter(is_active=True),
                many=True
            ).data,

            # Тарифы
            'pricing': PricingPlanSerializer(
                PricingPlan.objects.filter(is_active=True),
                many=True
            ).data,
        }
        return Response(data)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для курсов (только чтение)"""
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'total_students', 'average_rating']
    ordering = ['order']





class LeadViewSet(viewsets.ModelViewSet):
    """ViewSet для лидов"""
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Если пользователь авторизован, связываем заявку с ним
        if request.user.is_authenticated:
            serializer.save(user=request.user)
        else:
            serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
