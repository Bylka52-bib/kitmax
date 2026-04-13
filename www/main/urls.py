"""
Маршрутизация API для приложения main.
Используем DefaultRouter для автоматической генерации RESTful маршрутов.

Согласно ТЗ: API-first архитектура, все эндпоинты доступны по /api/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from .views import (
    # Аутентификация
    RegisterView, LoginView, IndexView,
    # ViewSets
    UserViewSet, AuthorViewSet, BookViewSet,
    PlatformStatisticsViewSet, HeroBlockViewSet,
    StudentBlockViewSet, TeacherBlockViewSet,
    ScreenshotViewSet, TestimonialViewSet,
    PricingPlanViewSet, LeadViewSet,
    # Объединенный эндпоинт
    LandingPageAPIView, CourseViewSet
)

# Создаем роутер для автоматической генерации маршрутов
router = DefaultRouter()

# Регистрируем все ViewSet'ы
router.register(r'users', UserViewSet, basename='users')
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'statistics', PlatformStatisticsViewSet, basename='statistics')
router.register(r'hero', HeroBlockViewSet, basename='hero')
router.register(r'student-blocks', StudentBlockViewSet, basename='student-blocks')
router.register(r'teacher-blocks', TeacherBlockViewSet, basename='teacher-blocks')
router.register(r'screenshots', ScreenshotViewSet, basename='screenshots')
router.register(r'testimonials', TestimonialViewSet, basename='testimonials')
router.register(r'pricing', PricingPlanViewSet, basename='pricing')
router.register(r'leads', LeadViewSet, basename='leads')
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    # Все маршруты от роутера
    path('', include(router.urls)),

    # Объединенный эндпоинт для лендинга
    path('landing/', LandingPageAPIView.as_view(), name='landing-page'),

    # Эндпоинты аутентификации
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index'),

]
