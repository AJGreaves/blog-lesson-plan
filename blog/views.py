from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

# Create your views here.


class PostList(generic.ListView):
    """
    This is Django's generic ListView. We are a little limited as to
    what we can do with this, but if we really needed to, we could
    access the request object here too.

    It's a class, which is why we had used class-based views in the
    original blog material. Now, to show what's going on under the
    hood, so to speak, we'll use function-based ones instead.
    """

    model = Post
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug, *args, **kwargs):
    """
    A function-based view to view the detail of a post.
    Largely the same as the class-based, but it is a bit
    clearer what's going on.
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    # this works and is simpler...
    # post = get_object_or_404(Post, slug=slug, status=1)

    return render(
        request,
        "blog/post_detail.html",
        {"post": post},
    )
