from django.views.generic import DetailView, ListView

from blogs.models import Blog


class BlogListView(ListView):
    """Контроллер для вывода списка блогов"""

    model = Blog
    template_name = "blogs/index.html"


class BlogDetailView(DetailView):
    """Контроллер для просмотра блога"""

    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
