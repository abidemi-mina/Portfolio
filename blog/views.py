from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Post
from .forms import CommentForm
from .services import PostService, ExternalLinkService


class PostListView(ListView):
    template_name    = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by      = 9

    def get_queryset(self):
        return PostService.get_published()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['external_links'] = ExternalLinkService.get_active()
        ctx['page_title']     = f'Writing — {{}}'
        return ctx


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
            ctx['page_title']    = f'{self.object.title}'
        return ctx


class LikeToggleView(View):
    """AJAX POST — toggles like, returns JSON {liked, count}."""

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, is_published=True)
        ip   = PostService.get_client_ip(request)
        liked, count = PostService.toggle_like(post, ip)
        return JsonResponse({'liked': liked, 'count': count})


class CommentCreateView(View):
    """POST — saves comment (unapproved). Redirects back to post."""

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, is_published=True)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment      = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url() + '?commented=1#comments')
        # Invalid — redirect back (form errors lost, acceptable for simplicity)
        return redirect(post.get_absolute_url() + '#comment-form')
