from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, IndexView,
    UserViewSet, AuthorViewSet, BookViewSet,
    PlatformStatisticsViewSet, HeroBlockViewSet,
    StudentBlockViewSet, TeacherBlockViewSet,
    ScreenshotViewSet, TestimonialViewSet,
    PricingPlanViewSet, LeadViewSet,
    LandingPageAPIView, CourseViewSet
)

router = DefaultRouter()

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
    path('', include(router.urls)),
    path('landing/', LandingPageAPIView.as_view(), name='landing-page'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index'),

]
