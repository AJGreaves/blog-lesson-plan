from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm

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
    liked = False
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    comment_form = CommentForm()

    if post.likes.filter(id=request.user.id).exists():
        liked = True

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "liked": liked,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def post_like(request, slug, *args, **kwargs):
    """
    The view to update the likes. Although it should always be
    called using the POST method, we have still added some
    defensive programming to make sure.
    """
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST" and request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
