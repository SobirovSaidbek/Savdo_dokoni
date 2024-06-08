from django.views.generic import ListView, DetailView

from blogs.models import BlogModel, BlogCategoryModel, BlogTagModel


class BlogListView(ListView):
    template_name = 'blogs/blog-list.html'
    context_object_name = 'blogs'
    paginate_by = 2

    def get_queryset(self):
        qs = BlogModel.objects.all().order_by('-pk')
        cat = self.request.GET.get('cat')
        tag = self.request.GET.get('tag')

        if cat:
            qs = qs.filter(categories=cat)
        if tag:
            qs = qs.filter(tags=tag)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategoryModel.objects.all()
        context['tags'] = BlogTagModel.objects.all()
        context['famous_blogs'] = BlogModel.objects.all().order_by('-created_at')[:2]

        return context


class BlogDetailView(DetailView):
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blog'
    model = BlogModel

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            "categories": BlogCategoryModel.objects.all(),
            "blog": BlogModel.objects.get(pk=self.kwargs['pk']),
            "tags": BlogTagModel.objects.all(),
            "famous_blogs": BlogModel.objects.all().order_by('-created_at')[:2],
            "related_blogs": BlogModel.objects.filter(categories__in=self.object.categories.all()).order_by(
                '-created_at')[:3]
        }
        return context
