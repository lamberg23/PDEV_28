# Проект приложения NewsPortal
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


#модель автор поста/статьи
class Author(models.Model):
    author = models.OneToOneField(User,on_delete = models.CASCADE)
    rate = models.IntegerField(default=0)

# расчет рэйтинга автора
    def update_rating(self):
        post_rate = Post.objects.filter(author=self).aggregate(result1=Sum('rate')).get('result1')
        comment_author = Comment.objects.filter(post__author=self).aggregate(result2=Sum('rate')).get('result2')
        comment_rate = Comment.objects.filter(user=self.author).aggregate(result3=Sum('rate')).get('result3')

        self.rate = 3*post_rate + comment_author +comment_rate
        self.save()

# модель категория статьи -  категории строго уникальны
class Category(models.Model):
    post_category = models.CharField(max_length=255,unique=True)

#модель статья/новость. Связь с автором, может иметь несколько категорий
class Post(models.Model):
    post = 'post'
    news = 'news'

    TYPES = [
        (post, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=4,
                                choices=TYPES,
                                default=post)
    time_in = models.DateTimeField(auto_now_add=True)
    head = models.CharField(max_length=255)
    text = models.TextField()
    rate = models.IntegerField(default=0.0)
    post_category = models.ManyToManyField(Category,through='PostCategory')

# увеличение рэйтинга на 1
    def like(self):
        self.rate +=1
        self.save()

# снижение рейтинга на 1
    def dislike(self):
        self.rate -= 1
        self.save()
# функция вывода краткого начала статьи
    def preview(self):
        prev_text = self.text[0:124]+'...'
        return prev_text

# модель комментарии - связь со статьей, пользователем
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0.0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()
# таблица связей многие ко многим (статья-категории)
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




