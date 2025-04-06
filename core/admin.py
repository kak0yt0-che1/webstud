from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Course, Module, Lesson, UserLessonProgress

# Курсы, уроки, модули
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)

# Inline для отображения прогресса прямо у пользователя
class ProgressInline(admin.TabularInline):
    model = UserLessonProgress
    extra = 0

# Расширяем UserAdmin
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

# Админка для прогресса
@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'completed_at')
    search_fields = ('user__username', 'lesson__title')
