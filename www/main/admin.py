from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Course, Testimonial, Lead, PlatformStatistics,
    HeroBlock, StudentBlock, TeacherBlock, Screenshot,
    PricingPlan, Author, Book
)

from django.utils.html import format_html


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'platform_user_id', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'user_type', 'avatar', 'platform_user_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'get_author_name', 'platform_course_id', 'total_students', 'average_rating', 'order', 'is_featured',
        'is_active')
    list_filter = ('is_featured', 'is_active', 'author')
    search_fields = ('title', 'platform_course_id', 'author__name')
    list_editable = ('order', 'is_featured', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

    def get_author_name(self, obj):
        return obj.get_author_name()

    get_author_name.short_description = 'Автор'

    fieldsets = (
        ('Основная информация', {
            'fields': ('platform_course_id', 'title', 'description', 'short_description')
        }),
        ('Медиа', {
            'fields': ('cover_image', 'preview_video')
        }),
        ('Автор', {
            'fields': ('author',)
        }),
        ('Статистика', {
            'fields': ('total_students', 'average_rating')
        }),
        ('Настройки отображения', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'course', 'rating', 'is_verified', 'is_active', 'created_at')
    list_filter = ('rating', 'is_verified', 'is_active', 'course')
    search_fields = ('user__email', 'guest_name', 'guest_email', 'content')
    list_editable = ('is_verified', 'is_active')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Автор', {
            'fields': ('user', 'guest_name', 'guest_email')
        }),
        ('О курсе', {
            'fields': ('course', 'rating', 'content')
        }),
        ('Статус', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'user_type', 'course', 'status', 'created_at')
    list_filter = ('user_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Контактные данные', {
            'fields': ('name', 'email', 'phone', 'user_type')
        }),
        ('Интерес', {
            'fields': ('course', 'message')
        }),
        ('Связь с пользователем', {
            'fields': ('user',)
        }),
        ('Обработка', {
            'fields': ('status', 'comment')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PlatformStatistics)
class PlatformStatisticsAdmin(admin.ModelAdmin):
    list_display = ('active_courses', 'total_students', 'total_teachers', 'completed_duels', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(HeroBlock)
class HeroBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text', 'is_active')
    list_filter = ('is_active',)


@admin.register(StudentBlock)
class StudentBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'icon_preview')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    filter_horizontal = ('featured_courses',)
    readonly_fields = ('icon_preview',)

    fields = ('title', 'description', 'icon', 'icon_preview', 'featured_courses', 'order', 'is_active')

    def icon_preview(self, obj):
        if obj.icon:
            if obj.icon.name.lower().endswith('.svg'):
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.icon.url)
            else:
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.icon.url)
        return "Нет иконки"

    icon_preview.short_description = 'Превью иконки'


@admin.register(TeacherBlock)
class TeacherBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'icon_preview')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('icon_preview',)

    fields = ('title', 'description', 'icon', 'icon_preview', 'feature_link', 'order', 'is_active')

    def icon_preview(self, obj):
        if obj.icon:
            if obj.icon.name.lower().endswith('.svg'):
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.icon.url)
            else:
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.icon.url)
        return "Нет иконки"

    icon_preview.short_description = 'Превью иконки'


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'course', 'order', 'is_active')
    list_filter = ('section', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_period', 'is_popular', 'is_active', 'order')
    list_filter = ('is_popular', 'is_active')
    list_editable = ('order', 'is_popular', 'is_active')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pages', 'price', 'is_active')
    list_filter = ('is_active', 'author')
    search_fields = ('title', 'author__name')
    list_editable = ('price', 'is_active')
