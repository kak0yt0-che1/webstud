from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Course, Module, Lesson, UserLessonProgress

# --- Курсы с фильтрами по языку ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'created_at')
    list_filter = ('language',)
    search_fields = ('title', 'description')

# --- Модули и уроки ---
admin.site.register(Module)
admin.site.register(Lesson)

# --- Inline для отображения прогресса у пользователя ---
class ProgressInline(admin.TabularInline):
    model = UserLessonProgress
    extra = 0

# --- Кастомный UserAdmin ---
class CustomUserAdmin(UserAdmin):
    inlines = [ProgressInline]
    list_display = ('username', 'email', 'is_subscribed', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Подписка', {'fields': ('is_subscribed',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Подписка', {'fields': ('is_subscribed',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# --- Админка для прогресса пользователя ---
@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'completed_at')
    search_fields = ('user__username', 'lesson__title')
