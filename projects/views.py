from django.views.generic import ListView, DetailView
from .models import Project
from .services import ProjectQueryService


class ProjectListView(ListView):
    template_name    = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by      = 6

    def get_queryset(self):
        return ProjectQueryService.get_all_with_filters(
            category_slug=self.request.GET.get('category', ''),
            query=self.request.GET.get('q', ''),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories']  = ProjectQueryService.get_all_categories()
        context['category_filter'] = self.request.GET.get('category', '')
        context['search_query']    = self.request.GET.get('q', '')
        context['page_title']      = 'Projects — MinaDXplorer'

        # Build query string WITHOUT ?page so pagination links can append &page=N
        qp = self.request.GET.copy()
        qp.pop('page', None)
        context['query_string'] = ('&' + qp.urlencode()) if qp else ''

        # Numbered pagination with elision (1 2 … 5 6 7 … 12 13)
        context['page_range'] = context['paginator'].get_elided_page_range(
            context['page_obj'].number, on_each_side=2, on_ends=1
        )
        return context


class ProjectDetailView(DetailView):
    template_name       = 'projects/detail.html'
    context_object_name = 'project'

    def get_object(self):
        return ProjectQueryService.get_detail(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            first_cat = self.object.categories.first()
            related   = ProjectQueryService.get_published().exclude(pk=self.object.pk)
            if first_cat:
                related = related.filter(categories=first_cat)
            context['related_projects'] = related[:3]
            context['page_title']       = f'{self.object.title} — MinaDXplorer'
        return context
