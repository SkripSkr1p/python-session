from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserRegistrationForm, UserLoginForm


def home(request):
    """Главная страница с последними объявлениями"""
    posts = Post.objects.filter(status='published').order_by('-created_at')[:10]
    categories = Category.objects.all()
    return render(request, 'posts/home.html', {
        'posts': posts,
        'categories': categories
    })


def post_list(request):
    """Список всех объявлений с фильтрацией и поиском"""
    posts = Post.objects.filter(status='published')
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query
    })


def post_detail(request, pk):
    """Детальная страница объявления"""
    post = get_object_or_404(Post, pk=pk, status='published')
    
    # Увеличиваем счетчик просмотров
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    comments = post.comments.filter(is_active=True).order_by('created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, 'Комментарий добавлен!')
                return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Необходимо войти в систему для добавления комментариев.')
    else:
        comment_form = CommentForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def post_create(request):
    """Создание нового объявления"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Объявление создано!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Создать объявление'
    })


@login_required
def post_edit(request, pk):
    """Редактирование объявления"""
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Редактировать объявление',
        'post': post
    })


@login_required
def post_delete(request, pk):
    """Удаление объявления"""
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Объявление удалено!')
        return redirect('post_list')
    
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def user_register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Аккаунт создан для {username}!')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Ошибка при создании аккаунта: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'posts/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверные учетные данные.')
    else:
        form = UserLoginForm()
    
    return render(request, 'posts/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


@login_required
def my_posts(request):
    """Мои объявления"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'posts/my_posts.html', {'page_obj': page_obj})
