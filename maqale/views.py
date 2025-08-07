from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, CommentLike,RegisteredUser
from .forms import CommentForm,UserRegisterForms
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'maqale/maqale.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.filter(parent__isnull=True).order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post

                parent_id = request.POST.get('parent_id')
                if parent_id:
                  
                    parent_comment = get_object_or_404(Comment, pk=parent_id)
                    comment.parent = parent_comment

                comment.save()
                return redirect('maqale:post_detail', pk=post.pk)
        else:
            return redirect('maqle:login')
    else:
        form = CommentForm()

    return render(request, 'maqale/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required(login_url='login')
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('maqale:post_detail', pk=comment.post.pk)




def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForms(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            new_user = RegisteredUser.objects.create(
                user_name=cd['user_name'],
                email=cd['email'],
                password=cd['password_1'],
            )
            
            
            return redirect('login')
    else:
        form = UserRegisterForms()
    return render(request, 'registration/register.html', {'form': form})

