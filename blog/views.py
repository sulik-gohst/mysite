from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm, EmailForm



def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('blog:post_list')
    return render(request, 'blog/post/create.html', {'form': form})


def post_list(request):
    object_list = Post.object.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}({cd['email']}), recomends you reading "\
                      f"{post.title}"
            message = f"Read '{post.title}' at {post_url}" \
                      f"where {cd['name']} comment {cd['comments']}"
            send_mail(subject, message, 'myrzakanovsultan0@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
