from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, Author, Book, PlatformStatistics, HeroBlock, StudentBlock, TeacherBlock,
    Screenshot, Testimonial, PricingPlan, Lead, Course
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'user_type', 'avatar')
        read_only_fields = ('id',)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'user_type')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'created_at')
        read_only_fields = ('id', 'created_at')


class BookSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для чтения
    author_detail = AuthorSerializer(source='author', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'author_detail', 'pages', 'price',
                  'published_date', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_title(self, value):
        """Field-level validation"""
        if len(value) < 2:
            raise serializers.ValidationError("Название книги должно содержать минимум 2 символа")
        return value

    def validate_pages(self, value):
        """Field-level validation for pages"""
        if value <= 0:
            raise serializers.ValidationError("Количество страниц должно быть положительным числом")
        if value > 10000:
            raise serializers.ValidationError("Количество страниц не может превышать 10000")
        return value

    def validate(self, data):
        """Object-level validation"""
        # Проверка, что если книга дорогая, то она должна быть активной
        if data.get('price', 0) > 10000 and not data.get('is_active', True):
            raise serializers.ValidationError({
                "is_active": "Дорогие книги должны быть активными"
            })
        return data


class PlatformStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformStatistics
        fields = ('active_courses', 'total_students', 'total_teachers', 'completed_duels', 'updated_at')


class HeroBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBlock
        fields = ('id', 'title', 'subtitle', 'background_image', 'button_text', 'button_link')


class StudentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentBlock
        fields = ('id', 'title', 'description', 'icon', 'order')


class TeacherBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherBlock
        fields = ('id', 'title', 'description', 'icon', 'feature_link', 'order')


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ('id', 'title', 'image', 'section', 'order')





class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = ('id', 'name', 'price', 'price_period', 'features', 'is_popular')



class CourseSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_detail = AuthorSerializer(source='author', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'platform_course_id', 'title', 'description', 'short_description',
                  'cover_image', 'preview_video', 'author', 'author_name', 'author_detail',
                  'total_students', 'average_rating', 'is_featured', 'order',
                  'is_active', 'created_at', 'updated_at')

    def get_author_name(self, obj):
        return obj.get_author_name()


class TestimonialSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    display_name = serializers.ReadOnlyField()
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Testimonial
        fields = ('id', 'user', 'course', 'course_title', 'guest_name', 'guest_email',
                  'content', 'rating', 'is_verified', 'is_active', 'display_name', 'created_at')
        read_only_fields = ('id', 'created_at', 'is_verified')


class LeadSerializer(serializers.ModelSerializer):
    """Сериализатор для лидов"""

    class Meta:
        model = Lead
        fields = ('id', 'user', 'course', 'name', 'email', 'phone', 'user_type',
                  'message', 'status', 'created_at')
        read_only_fields = ('id', 'created_at', 'status')

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email обязателен")
        return value

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Номер телефона обязателен")
        phone_digits = ''.join(filter(str.isdigit, value))
        if len(phone_digits) < 10:
            raise serializers.ValidationError("Номер телефона должен содержать минимум 10 цифр")
        return value