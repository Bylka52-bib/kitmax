from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
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
from .pagination import StandardResultsSetPagination
from .filters import BookFilter

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(generics.CreateAPIView):
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


class UserViewSet(viewsets.ModelViewSet):
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
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
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


class BookViewSet(viewsets.ModelViewSet):
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


class PlatformStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformStatistics.objects.all()
    serializer_class = PlatformStatisticsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return PlatformStatistics.objects.order_by('-updated_at')[:1]


class HeroBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HeroBlock.objects.filter(is_active=True)
    serializer_class = HeroBlockSerializer
    permission_classes = [permissions.AllowAny]


class StudentBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentBlock.objects.filter(is_active=True)
    serializer_class = StudentBlockSerializer
    permission_classes = [permissions.AllowAny]


class TeacherBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeacherBlock.objects.filter(is_active=True)
    serializer_class = TeacherBlockSerializer
    permission_classes = [permissions.AllowAny]


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ScreenshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Screenshot.objects.filter(is_active=True)
    serializer_class = ScreenshotSerializer
    permission_classes = [AllowAny]


class PricingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PricingPlan.objects.filter(is_active=True)
    serializer_class = PricingPlanSerializer
    permission_classes = [permissions.AllowAny]


class LandingPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = {
            'hero': HeroBlockSerializer(
                HeroBlock.objects.filter(is_active=True).first()
            ).data if HeroBlock.objects.filter(is_active=True).exists() else None,

            'student_blocks': StudentBlockSerializer(
                StudentBlock.objects.filter(is_active=True),
                many=True
            ).data,

            'teacher_blocks': TeacherBlockSerializer(
                TeacherBlock.objects.filter(is_active=True),
                many=True
            ).data,

            'statistics': PlatformStatisticsSerializer(
                PlatformStatistics.objects.order_by('-updated_at').first()
            ).data if PlatformStatistics.objects.exists() else None,

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
            'testimonials': TestimonialSerializer(
                Testimonial.objects.filter(is_active=True),
                many=True
            ).data,

            'pricing': PricingPlanSerializer(
                PricingPlan.objects.filter(is_active=True),
                many=True
            ).data,
        }
        return Response(data)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'total_students', 'average_rating']
    ordering = ['order']


class LeadViewSet(viewsets.ModelViewSet):
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
