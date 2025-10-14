from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Category, Post, Comment
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        # Создаем пользователей
        if not User.objects.filter(username='testuser1').exists():
            user1 = User.objects.create_user(
                username='testuser1',
                email='test1@example.com',
                password='testpass123',
                first_name='Иван',
                last_name='Петров'
            )
            self.stdout.write(f'Создан пользователь: {user1.username}')
        else:
            user1 = User.objects.get(username='testuser1')

        if not User.objects.filter(username='testuser2').exists():
            user2 = User.objects.create_user(
                username='testuser2',
                email='test2@example.com',
                password='testpass123',
                first_name='Мария',
                last_name='Сидорова'
            )
            self.stdout.write(f'Создан пользователь: {user2.username}')
        else:
            user2 = User.objects.get(username='testuser2')

        # Создаем категории
        categories_data = [
            {'name': 'Недвижимость', 'description': 'Квартиры, дома, участки'},
            {'name': 'Транспорт', 'description': 'Автомобили, мотоциклы, велосипеды'},
            {'name': 'Электроника', 'description': 'Телефоны, компьютеры, бытовая техника'},
            {'name': 'Одежда и обувь', 'description': 'Мужская, женская, детская одежда'},
            {'name': 'Мебель', 'description': 'Диваны, столы, шкафы, кровати'},
            {'name': 'Спорт и отдых', 'description': 'Спортивный инвентарь, туризм'},
            {'name': 'Животные', 'description': 'Собаки, кошки, птицы, рыбы'},
            {'name': 'Услуги', 'description': 'Ремонт, обучение, консультации'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

        # Создаем объявления
        posts_data = [
            {
                'title': 'Продам 2-комнатную квартиру в центре',
                'content': 'Продается 2-комнатная квартира в центре города. Отличное состояние, евроремонт. Рядом метро, школы, магазины. Собственник.',
                'category': 'Недвижимость',
                'price': 4500000,
                'contact_phone': '+7 (999) 123-45-67',
                'contact_email': 'apartment@example.com',
                'author': user1,
                'status': 'published'
            },
            {
                'title': 'BMW X5 2018 года',
                'content': 'Продаю BMW X5 2018 года выпуска. Пробег 45000 км. Полный привод, автоматическая коробка. В отличном состоянии. Все документы в порядке.',
                'category': 'Транспорт',
                'price': 2800000,
                'contact_phone': '+7 (999) 234-56-78',
                'contact_email': 'bmw@example.com',
                'author': user2,
                'status': 'published'
            },
            {
                'title': 'iPhone 14 Pro 128GB',
                'content': 'Продаю iPhone 14 Pro 128GB, цвет Space Black. Покупка в официальном магазине Apple. Гарантия до конца года. В идеальном состоянии.',
                'category': 'Электроника',
                'price': 85000,
                'contact_phone': '+7 (999) 345-67-89',
                'contact_email': 'iphone@example.com',
                'author': user1,
                'status': 'published'
            },
            {
                'title': 'Кожаная куртка мужская',
                'content': 'Кожаная куртка мужская, размер 50. Натуральная кожа. Носил мало, состояние отличное. Бренд Zara.',
                'category': 'Одежда и обувь',
                'price': 15000,
                'contact_phone': '+7 (999) 456-78-90',
                'author': user2,
                'status': 'published'
            },
            {
                'title': 'Диван-кровать раскладной',
                'content': 'Продаю диван-кровать раскладной. Цвет серый. Состояние хорошее. Подходит для гостиной или спальни. Самовывоз.',
                'category': 'Мебель',
                'price': 25000,
                'contact_phone': '+7 (999) 567-89-01',
                'author': user1,
                'status': 'published'
            },
            {
                'title': 'Велосипед горный Trek',
                'content': 'Горный велосипед Trek. 21 скорость, амортизаторы. Отлично подходит для поездок по городу и за город. Состояние хорошее.',
                'category': 'Спорт и отдых',
                'price': 35000,
                'contact_phone': '+7 (999) 678-90-12',
                'author': user2,
                'status': 'published'
            },
            {
                'title': 'Щенок лабрадора',
                'content': 'Продаю щенка лабрадора, возраст 2 месяца. Привит, приучен к лотку. Очень дружелюбный и игривый. Родители с документами.',
                'category': 'Животные',
                'price': 45000,
                'contact_phone': '+7 (999) 789-01-23',
                'contact_email': 'puppy@example.com',
                'author': user1,
                'status': 'published'
            },
            {
                'title': 'Ремонт компьютеров',
                'content': 'Предлагаю услуги по ремонту компьютеров и ноутбуков. Диагностика, замена комплектующих, установка программ. Выезд на дом.',
                'category': 'Услуги',
                'price': 2000,
                'contact_phone': '+7 (999) 890-12-34',
                'contact_email': 'repair@example.com',
                'author': user2,
                'status': 'published'
            },
            {
                'title': 'MacBook Pro 13" M1',
                'content': 'Продаю MacBook Pro 13" с чипом M1. 8GB RAM, 256GB SSD. В отличном состоянии, все работает идеально. С оригинальной зарядкой.',
                'category': 'Электроника',
                'price': 120000,
                'contact_phone': '+7 (999) 901-23-45',
                'author': user1,
                'status': 'published'
            },
            {
                'title': 'Квартира-студия в новостройке',
                'content': 'Продается квартира-студия в новостройке. Современная планировка, панорамные окна. Рядом парк и метро. Рассрочка возможна.',
                'category': 'Недвижимость',
                'price': 3200000,
                'contact_phone': '+7 (999) 012-34-56',
                'contact_email': 'studio@example.com',
                'author': user2,
                'status': 'published'
            }
        ]

        for post_data in posts_data:
            category = next(cat for cat in categories if cat.name == post_data['category'])
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'category': category,
                    'price': Decimal(str(post_data['price'])),
                    'contact_phone': post_data.get('contact_phone', ''),
                    'contact_email': post_data.get('contact_email', ''),
                    'author': post_data['author'],
                    'status': post_data['status']
                }
            )
            if created:
                self.stdout.write(f'Создано объявление: {post.title}')

        # Создаем комментарии
        comments_data = [
            {
                'post_title': 'Продам 2-комнатную квартиру в центре',
                'content': 'Интересное предложение! Можно ли посмотреть квартиру в выходные?',
                'author': user2
            },
            {
                'post_title': 'BMW X5 2018 года',
                'content': 'Отличная машина! Сколько владельцев было?',
                'author': user1
            },
            {
                'post_title': 'iPhone 14 Pro 128GB',
                'content': 'Цена актуальна? Есть ли чеки?',
                'author': user2
            },
            {
                'post_title': 'Щенок лабрадора',
                'content': 'Очень милый щенок! Есть ли документы на родителей?',
                'author': user2
            },
            {
                'post_title': 'Ремонт компьютеров',
                'content': 'Сколько времени занимает диагностика?',
                'author': user1
            }
        ]

        for comment_data in comments_data:
            try:
                post = Post.objects.get(title=comment_data['post_title'])
                comment, created = Comment.objects.get_or_create(
                    post=post,
                    author=comment_data['author'],
                    content=comment_data['content']
                )
                if created:
                    self.stdout.write(f'Создан комментарий к объявлению: {post.title}')
            except Post.DoesNotExist:
                pass

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!')
        )
        self.stdout.write('Создано:')
        self.stdout.write(f'- Пользователей: {User.objects.count()}')
        self.stdout.write(f'- Категорий: {Category.objects.count()}')
        self.stdout.write(f'- Объявлений: {Post.objects.count()}')
        self.stdout.write(f'- Комментариев: {Comment.objects.count()}')
        self.stdout.write('')
        self.stdout.write('Тестовые пользователи:')
        self.stdout.write('- Логин: testuser1, Пароль: testpass123')
        self.stdout.write('- Логин: testuser2, Пароль: testpass123')
