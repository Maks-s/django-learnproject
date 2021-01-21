from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView

from .forms import PostForm
from .models import Post

class PostListView(ListView):
    model = Post
    paginate_by = 2
    queryset = Post.objects.order_by('-created_date')

    def get(self, request):
        return super().get(self, request)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    login_url = '/admin/login'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreateView, self).form_valid(form)

class PostDetailView(DetailView):
    model = Post
