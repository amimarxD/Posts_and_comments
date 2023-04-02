from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostingForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required(login_url='/login/?next=/post')
def index(request):
    latest_post_list = Post.objects.all().order_by("-created_at")[:10]
    
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        user_id = request.POST.get("user_id")
        if post_id:
            post = Post.objects.get(id = post_id)
            if post and (post.author == request.user or request.user.has_perm("posts_and_comments.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.get(id=user_id)
            print(user)
            if user and request.user.is_staff:
                group = Group.objects.get(name='default')
                group.user_set.remove(user)

                group = Group.objects.get(name='mod')
                group.user_set.remove(user)

    return render(request, "posts_and_comments/index.html", {'latest_post_list' : latest_post_list})

# class IndexView(LoginRequiredMixin, generic.ListView):
#     template_name = "posts_and_comments/index.html"
#     context_object_name = "latest_post_list"
#     login_url = "/login/?next=/post"

#     def get_queryset(self):
#         """
#             Return the last ten published questions and the last comment on that post.
#         """

#         return Post.objects.all().order_by("-created_at")[:10]

@permission_required("posts_and_comments.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('post:index'))
    else:
        form = PostingForm()

    return render(request, "posts_and_comments/create_post.html", {"form": form})

    