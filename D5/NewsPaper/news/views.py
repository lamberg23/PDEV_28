from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm

# Create your views here.


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2

class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'

# Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель стаьи
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'news'
        return super().form_valid(form)

class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель стаьи
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'article'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')