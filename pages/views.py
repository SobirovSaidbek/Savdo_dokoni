from django.views.generic import TemplateView, CreateView
from pages.models import UserCommentModel
from pages.form import ContactModelForm


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = {
            'user_comments': UserCommentModel.objects.all()
        }
        return context


class ContactTemplateView(CreateView):
    template_name = 'contact.html'
    form_class = ContactModelForm
    success_url = '/'

