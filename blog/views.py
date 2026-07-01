from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Post
from .forms import CommentForm
from .services import PostService, ExternalLinkService


EXTERNAL_LINKS_PER_PAGE = 6


class PostListView(ListView):
    template_name       = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by         = 6
    page_kwarg          = 'page'

    def get_queryset(self):
        return PostService.get_published()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Writing — MinaDXplorer'

        # --- Posts pagination ---
        ctx['page_range'] = ctx['paginator'].get_elided_page_range(
            ctx['page_obj'].number, on_each_side=2, on_ends=1
        )
        ctx['query_string'] = self._sibling_query_string(exclude='page')

        # --- External links pagination ---
        el_paginator = Paginator(ExternalLinkService.get_active(), EXTERNAL_LINKS_PER_PAGE)
        el_page_obj  = el_paginator.get_page(self.request.GET.get('elpage', 1))

        ctx['external_links']        = el_page_obj
        ctx['external_page_obj']     = el_page_obj
        ctx['external_page_range']   = el_paginator.get_elided_page_range(
            el_page_obj.number, on_each_side=2, on_ends=1
        )
        ctx['external_query_string'] = self._sibling_query_string(exclude='elpage')

        return ctx

    def _sibling_query_string(self, exclude):
        """Preserve every GET param except the one this paginator owns."""
        params = self.request.GET.copy()
        params.pop(exclude, None)
        return f'&{params.urlencode()}' if params else ''


class PostDetailView(DetailView):
    template_name       = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self):
        return PostService.get_detail(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object:
            ip = PostService.get_client_ip(self.request)
            ctx['rendered_body'] = PostService.get_rendered_body(self.object)
            ctx['comments']      = PostService.get_approved_comments(self.object)
            ctx['comment_form']  = CommentForm()
            ctx['has_liked']     = PostService.has_liked(self.object, ip)
            ctx['like_count']    = self.object.like_count()
            ctx['page_title']    = self.object.title
        return ctx


class LikeToggleView(View):
    def post(self, request, slug):
        post  = get_object_or_404(Post, slug=slug, is_published=True)
        ip    = PostService.get_client_ip(request)
        liked, count = PostService.toggle_like(post, ip)
        return JsonResponse({'liked': liked, 'count': count})


class CommentCreateView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, is_published=True)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment      = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url() + '?commented=1#comments')
        return redirect(post.get_absolute_url() + '#comment-form')