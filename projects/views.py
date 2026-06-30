from django.views.generic import ListView, DetailView
from .models import Project
from .services import ProjectQueryService


class ProjectListView(ListView):
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        return ProjectQueryService.get_all_with_filters(
            category_slug=self.request.GET.get('category', ''),
            query=self.request.GET.get('q', ''),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = ProjectQueryService.get_all_categories()
        context['category_filter'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['page_title'] = 'Projects — MinaDXplorer'
        return context


class ProjectDetailView(DetailView):
    template_name = 'projects/detail.html'
    context_object_name = 'project'

    def get_object(self):
        return ProjectQueryService.get_detail(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            # Related: shares at least one category
            first_cat = self.object.categories.first()
            related = ProjectQueryService.get_published().exclude(pk=self.object.pk)
            if first_cat:
                related = related.filter(categories=first_cat)
            context['related_projects'] = related[:3]
            context['page_title'] = f'{self.object.title} — MinaDXplorer'
        return context
