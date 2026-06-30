from django.views.generic import FormView
from django.http import JsonResponse
from .forms import ContactForm
from .services import ContactService

class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        ContactService.process_submission(form, self.request)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': "Message received. I'll be in touch soon."})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return '/?contacted=1#contact'
