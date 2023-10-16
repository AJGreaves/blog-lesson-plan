from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
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
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        print("inside if request.method == 'POST'")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
            comment_form = CommentForm()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    print("Before return render()")
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def comment_edit(request, slug, comment_id, *args, **kwargs):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id, *args, **kwargs):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
