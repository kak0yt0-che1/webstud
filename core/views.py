from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CourseForm, ModuleForm, LessonForm, RegisterForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import Course, Module, UserLessonProgress, Lesson
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lessons.all()
    return render(request, 'core/module_detail.html', {
        'module': module,
        'lessons': lessons
    })

@csrf_exempt
@login_required
def uncomplete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lessons.all()

    for lesson in lessons:
        try:
            progress = UserLessonProgress.objects.get(user=request.user, lesson=lesson)
            progress.is_completed = False
            progress.save()
        except UserLessonProgress.DoesNotExist:
            continue

    return redirect('course_detail', course_id=module.course.id)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.prefetch_related('lessons')
    return render(request, 'core/course_detail.html', {
        'course': course,
        'modules': modules
    })

@csrf_exempt
@login_required
def complete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lessons.all()

    for lesson in lessons:
        progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'is_completed': True}
        )
        if not created and not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()

    return redirect('course_detail', course_id=module.course.id)

@login_required
def profile(request):
    courses = Course.objects.prefetch_related('modules__lessons')
    progress_data = []

    for course in courses:
        lessons = Lesson.objects.filter(module__course=course)
        total = lessons.count()

        completed = UserLessonProgress.objects.filter(
            user=request.user,
            lesson__in=lessons,
            is_completed=True
        ).count()

        percent = int((completed / total) * 100) if total > 0 else 0

        progress_data.append({
            'course': course,
            'total': total,
            'completed': completed,
            'percent': percent,
        })

    return render(request, 'core/profile.html', {'progress_data': progress_data})


@csrf_exempt
@login_required
def complete_lesson(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'is_completed': True}
        )
        if not created and not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

def index(request):
    return render(request, 'index.html')

@login_required
def add_course(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Доступ запрещён")
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

@login_required
def add_module(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Доступ запрещён")

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ModuleForm()

    return render(request, 'add_module.html', {'form': form})


@login_required
def add_lesson(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Доступ запрещён")

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = LessonForm()

    return render(request, 'add_lesson.html', {'form': form})

@login_required
def course_list(request):
    courses = Course.objects.all()
    q = request.GET.get('q')
    language = request.GET.get('language')

    if q:
        courses = courses.filter(title__icontains=q)
    if language:
        courses = courses.filter(language__iexact=language)  # ← 🔥 важно

    return render(request, 'courses.html', {'courses': courses})



@csrf_exempt
@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    result = None

    if request.method == 'POST' and lesson.task_type == 'test':
        user_answer = request.POST.get('test_answer', '').strip().lower()
        correct_answer = lesson.test_correct_answer.strip().lower() if lesson.test_correct_answer else ''
        result = (user_answer == correct_answer)

    return render(request, 'core/lesson_detail.html', {'lesson': lesson, 'result': result})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логиним
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('index')  # главная
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.used_temp_password = False
            request.user.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')  # или '/'
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/change_password.html', {'form': form})

def send_temp_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            temp_password = get_random_string(length=8)
            user.set_password(temp_password)
            user.used_temp_password = True  # ✅ важно!
            user.save()
            send_mail(
                'Временный пароль',
                f'Ваш временный пароль: {temp_password}',
                'noreply@webstudy.kz',
                [email],
                fail_silently=False,
            )
            return render(request, 'registration/temp_password_sent.html')
        except User.DoesNotExist:
            return render(request, 'registration/temp_password_form.html', {'error': 'Пользователь не найден'})
    return render(request, 'registration/temp_password_form.html')