import datetime
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from uuslug import slugify

from NewsPaper.app_news import models


class Command(BaseCommand):
    """
    Класс для заполнения базы случайными новостями.
    """
    help = 'create news'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.news_list = []

    def add_arguments(self, parser):
        """
        Добавление аргумента общего количества новостей, которые необходимо добавить.
        """
        parser.add_argument('total', type=int, help=u'Количество новых записей')

    def handle(self, *args, **kwargs):
        total_news = kwargs['total']

        start_implant = datetime.datetime.now()
        self.stdout.write(f"Началось добавление записей {start_implant}")

        authors = User.objects.filter(profile__is_verified=True)
        self.filling_news_list(total_news, authors)
        models.News.objects.bulk_create(self.news_list)
        self.create_news_for_each_author(authors)

        time_interval = datetime.datetime.now() - start_implant
        self.stdout.write(f"Добавлено {total_news} новых записей за {time_interval.seconds} секунд")

    def filling_news_list(self, total_news, authors):
        """
        Заполнение списка новостями.
        """

        for i in range(total_news):
            author = random.choice(authors)
            title = f'Название {i * random.randint(0, i)}'
            content = f'Содержание {i}' * random.randint(1, 1 + i)
            is_published = random.choice([True, False])
            published_at = None
            if is_published:
                published_at = timezone.now()
            slug = slugify(title)

            self.news_list.append(models.News(title=title,
                                              content=content,
                                              author=author,
                                              is_published=is_published,
                                              published_at=published_at,
                                              slug=slug, ))

    def create_news_for_each_author(self, authors):
        """
        Добавление по одной новости автору, чтобы прошел сигнал и
        автоматически обновилось опубликованное количество новостей
        """
        for author in authors:
            title = 'test'
            models.News.objects.create(title=title,
                                       content='content ' * 100,
                                       author=author,
                                       is_published=True,
                                       published_at=timezone.now(),
                                       slug=slugify(title), )
