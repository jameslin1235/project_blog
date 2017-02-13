from django.shortcuts import render,redirect,get_object_or_404
from sampleblog.models import Post, Comment, Profile, Category
from django.contrib.auth.models import User
from .forms import Draft_form, Register_form, Comment_form, Profile_form, Category_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def post_list(request):
    post_list = Post.objects.filter(published_date__isnull = False).order_by('-published_date')
    post_list_count = post_list.count()
    post_list_state = "posts"

    if post_list_count == 0:
        messages.info(request, 'There are no published posts yet.', extra_tags="alert alert-info")
        post_list_state = "post"
    if post_list_count == 1:
        post_list_state = "post"

    paginator = Paginator(post_list, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        post_list_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list_current_page = paginator.page(paginator.num_pages)

    context = {
    'post_list_current_page':post_list_current_page,
    'post_list_count':post_list_count,
    'post_list_state':post_list_state
    }
    return render(request,'sampleblog/post_list.html',context)



def post_details(request, post_slug):

    current_post = Post.objects.get(slug = post_slug)
    current_comments = Comment.objects.filter(post = current_post,parent__isnull=True).order_by('-created_date')
    current_comments_total = Comment.objects.filter(post = current_post).order_by('-created_date')
    current_comments_count = current_comments_total.count()
    current_comments_state = "comments"
    # current_replies = Comment.objects.filter(post = current_post,parent__isnull=False ).order_by('-created_date')
    # current_comments = Comment.objects.filter(post = current_post,parent__isnull=True).order_by('-created_date')
    # print(current_comments_no_parent.count())

    paginator = Paginator(current_comments, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        current_comments_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_comments_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_comments_current_page = paginator.page(paginator.num_pages)

    if request.method =='POST':
        comment_form = Comment_form(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = current_post
            parent_id = request.POST.get('parent_id')
            print(parent_id)
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            messages.info(request, 'Comment added.', extra_tags="alert alert-info")
            # return HttpResponseRedirect(reverse('post_list', ))
            return redirect('sampleblog:post_details',post_slug=current_post.slug)

    else:
        comment_form = Comment_form(auto_id=False)
        if current_comments_count == 0:
            messages.info(request, 'There are no comments yet.', extra_tags="alert alert-info")
            current_comments_state = "comment"
        if current_comments_count == 1:
            current_comments_state = "comment"

        context = {
        'current_post': current_post,
        'current_comments_current_page':current_comments_current_page,
        'current_comments_count':current_comments_count,
        'current_comments_total':current_comments_total,
        'current_comments_state':current_comments_state,
        'comment_form':comment_form
        }

        return render(request,'sampleblog/post_details.html',context)


def comment_like(request):

         comment_id = request.GET.get('comment_id')
         current_comment = Comment.objects.get(slug=comment_id)

         likes_count = current_comment.likes + 1
         current_comment.likes = likes_count
         current_comment.save()
         return HttpResponse(likes_count)

def comment_dislike(request):

         comment_id = request.GET.get('comment_id')
         current_comment = Comment.objects.get(slug=comment_id)

         dislikes_count = current_comment.dislikes + 1
         current_comment.dislikes = dislikes_count
         current_comment.save()
         return HttpResponse(dislikes_count)

def post_like(request):

         post_id = request.GET.get('post_id')
         current_post = Post.objects.get(slug=post_id)

         likes_count = current_post.likes + 1
         current_post.likes = likes_count
         current_post.save()
         return HttpResponse(likes_count)

def post_dislike(request):

         post_id = request.GET.get('post_id')
         current_post = Post.objects.get(slug=post_id)

         dislikes_count = current_post.dislikes + 1
         current_post.dislikes = dislikes_count
         current_post.save()
         return HttpResponse(dislikes_count)

def posts_by_category(request, category_slug):
    posts_by_category = Post.objects.filter(category__slug = category_slug,published_date__isnull = False).order_by('-published_date')
    posts_by_category_count = posts_by_category.count()
    posts_by_category_state = "posts"
    current_category = category_slug.title().replace("-"," ")


    if posts_by_category_count == 0:
        messages.info(request, 'This category does not have any posts yet.', extra_tags="alert alert-info")
        posts_by_category_state = "post"

    if posts_by_category_count == 1:
        posts_by_category_state = "post"

    paginator = Paginator(posts_by_category, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        posts_by_category_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts_by_category_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts_by_category_current_page = paginator.page(paginator.num_pages)

    context = {
    'posts_by_category_current_page':posts_by_category_current_page,
    'posts_by_category_count':posts_by_category_count,
    'current_category':current_category,
    'posts_by_category_state':posts_by_category_state
    }

    return render(request,'sampleblog/posts_by_category.html',context)



def category(request):

    category_field = Category._meta.get_field('category')
    category_field_choices = category_field.choices

    category_field_choices_list=[]
    category_field_choices_slug_list = []
    category_field_choices_count_list = []

    for x in category_field_choices:
        y = x[0]
        category_field_choices_list.append(y)

    for x in category_field_choices:
        y = slugify(x[0])
        category_field_choices_slug_list.append(y)

    for x in category_field_choices_list:
        posts_by_category = Post.objects.filter(category__category = x,published_date__isnull = False)
        posts_by_category_count = posts_by_category.count()
        category_field_choices_count_list.append(posts_by_category_count)


    category_field_choices_final_list =list(zip(category_field_choices_list, category_field_choices_slug_list,category_field_choices_count_list))

    print(category_field_choices_final_list)
    context = {
    'category_field_choices_final_list':category_field_choices_final_list,
    }

    return render(request,'sampleblog/category.html',context)

def posts_by_user(request, user):
    posts_by_user = Post.objects.filter(user__username = user,published_date__isnull = False).order_by('-published_date')
    current_user = user
    posts_by_user_state = 'posts'
    posts_by_user_count = posts_by_user.count()


    if posts_by_user_count == 0:
        posts_by_user_state = 'post'

    if posts_by_user_count == 1:
        posts_by_user_state = 'post'


    paginator = Paginator(posts_by_user, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        posts_by_user_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts_by_user_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts_by_user_current_page = paginator.page(paginator.num_pages)

    context = {
    'posts_by_user_current_page':posts_by_user_current_page,
    'current_user':current_user,
    'posts_by_user_count':posts_by_user_count,
    'posts_by_user_state':posts_by_user_state
    }
    return render(request,'sampleblog/posts_by_user.html',context)


def register(request):
    if request.method =='POST':
        register_form = Register_form(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            password = register_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # p = Profile.objects.create(user=user)
            return redirect('sampleblog:register_success')
        # else:
        #     print (register_form.errors)
    else:
        register_form = Register_form()

    context ={
    'register_form':register_form
    }
    return render(request,'sampleblog/register.html',context)

def register_success(request):
    return render(request,'sampleblog/register_success.html')




@login_required()
def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        current_user = User.objects.get(username = username)
        current_drafts = Post.objects.filter(published_date__isnull = True,user = current_user ).order_by('-created_date')[:3]
        current_posts = Post.objects.filter(published_date__isnull = False,user = current_user ).order_by('-published_date')[:3]
        current_comments = Comment.objects.filter(user = current_user).order_by('-created_date')[:3]
        current_drafts_count = current_drafts.count()
        current_posts_count = current_posts.count()
        current_comments_count = current_comments.count()
        if current_drafts_count == 0:
            messages.info(request, 'You have no drafts. Make one.', extra_tags="alert alert-info")
        if current_posts_count == 0:
            messages.info(request, 'You have no published posts. Make one.', extra_tags="alert alert-info")
        if current_comments_count == 0:
            messages.info(request, 'You have no comments. Make one.', extra_tags="alert alert-info")

        context={
        'current_user':current_user,
        'current_drafts':current_drafts,
        'current_posts':current_posts,
        'current_comments':current_comments,
        'current_drafts_count':current_drafts_count,
        'current_posts_count':current_posts_count,
        'current_comments_count':current_comments_count
        }

        return render(request,'sampleblog/dashboard.html',context)

@login_required()
def dashboard_drafts(request):
        username = request.user.username
        current_user = User.objects.get(username = username)
        current_drafts = Post.objects.filter(published_date__isnull = True, user = current_user).order_by('-created_date')
        current_drafts_count = current_drafts.count()
        if current_drafts_count == 0:
            messages.info(request, 'You have no drafts. Make one.', extra_tags="alert alert-info")

        paginator = Paginator(current_drafts, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_drafts_current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_drafts_current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_drafts_current_page = paginator.page(paginator.num_pages)

        context={
        'current_user':current_user,
        'current_drafts_current_page':current_drafts_current_page,
        'current_drafts_count':current_drafts_count
        }

        return render(request,'sampleblog/dashboard_drafts.html',context)

@login_required
def dashboard_drafts_add(request):
    if request.method == 'POST':
        draft_form = Draft_form(request.POST,prefix='draft')
        category_form = Category_form(request.POST,prefix='category')
        if draft_form.is_valid() and category_form.is_valid():
            draft = draft_form.save(commit=False)
            category = category_form.save()
            draft.category = category
            draft.user = request.user
            draft.save()
            messages.success(request, 'Draft added.',extra_tags="alert alert-success")
            return redirect('sampleblog:dashboard_drafts')
    else:
        draft_form = Draft_form(prefix='draft')
        category_form = Category_form(prefix='category')

        context ={
        'draft_form':draft_form,
        'category_form':category_form
        }

        return render(request,'sampleblog/dashboard_drafts_add.html',context)


@login_required
def dashboard_drafts_edit(request, draft_slug):
    current_draft = Post.objects.get(slug = draft_slug)
    current_category = current_draft.category

    if request.method =='POST':
        draft_form = Draft_form(request.POST,prefix='draft',instance=current_draft)
        category_form = Category_form(request.POST, prefix='category',instance=current_category)
        if draft_form.is_valid() and category_form.is_valid():
            category_form.save()
            draft_form.save()
            messages.success(request, 'Draft edited.',extra_tags="alert alert-success")
            return redirect('sampleblog:dashboard_drafts')
    else:
        draft_form = Draft_form(prefix='draft',instance=current_draft)
        category_form = Category_form(prefix='category',instance=current_category)

        context ={
        'draft_form':draft_form,
        'category_form':category_form
        }

        return render(request,'sampleblog/dashboard_drafts_edit.html',context)

@login_required
def dashboard_drafts_delete(request, draft_slug):
    current_draft = Post.objects.get(slug = draft_slug)
    current_draft.delete()
    current_draft.category.delete()
    messages.success(request, 'Draft deleted.',extra_tags="alert alert-success")
    return redirect('sampleblog:dashboard_drafts')

@login_required
def dashboard_drafts_publish(request, draft_slug):
    current_draft = Post.objects.get(slug = draft_slug)
    current_draft.published_date = timezone.now()
    current_draft.save()
    messages.success(request, 'Draft published.',extra_tags="alert alert-success")
    return redirect('sampleblog:dashboard_drafts')

@login_required
def dashboard_draft_details(request, draft_slug):

    current_draft = Post.objects.get(slug = draft_slug)

    context = {
    'current_draft': current_draft,
    }

    return render(request,'sampleblog/dashboard_draft_details.html',context)

@login_required
def dashboard_drafts_by_category(request, category_slug):
    username = request.user.username
    current_user = User.objects.get(username = username)
    drafts_by_category = Post.objects.filter(category__slug = category_slug, published_date__isnull = True, user = current_user).order_by('-created_date')
    drafts_by_category_count = drafts_by_category.count()
    current_category = category_slug.title().replace("-"," ")

    if drafts_by_category_count == 0:
        messages.info(request, 'This category does not have any drafts yet.', extra_tags="alert alert-info")

    paginator = Paginator(drafts_by_category, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        drafts_by_category_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        drafts_by_category_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        drafts_by_category_current_page = paginator.page(paginator.num_pages)

    context = {
    'drafts_by_category_current_page':drafts_by_category_current_page,
    'drafts_by_category_count':drafts_by_category_count,
    'current_category':current_category,
    }

    return render(request,'sampleblog/dashboard_drafts_by_category.html',context)

@login_required
def dashboard_drafts_by_user(request, user):
    drafts_by_user = Post.objects.filter(user__username = user, published_date__isnull = True).order_by('-created_date')
    current_user = user

    paginator = Paginator(drafts_by_user, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        drafts_by_user_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        drafts_by_user_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        drafts_by_user_current_page = paginator.page(paginator.num_pages)

    context = {
    'drafts_by_user_current_page':drafts_by_user_current_page,
    'current_user':current_user
    }
    return render(request,'sampleblog/dashboard_drafts_by_user.html',context)



@login_required
def dashboard_posts(request):
    username = request.user.username
    current_user = User.objects.get(username = username)
    current_posts = Post.objects.filter(published_date__isnull = False,user = current_user).order_by('-published_date')
    current_posts_count = current_posts.count()
    if current_posts_count == 0:
        messages.info(request, 'You have no published posts. Make one.', extra_tags="alert alert-info")

    paginator = Paginator(current_posts, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        current_posts_current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_posts_current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_posts_current_page = paginator.page(paginator.num_pages)

    context={
    'current_user':current_user,
    'current_posts_current_page':current_posts_current_page,
    'current_posts_count':current_posts_count
    }


    return render(request,'sampleblog/dashboard_posts.html',context)

@login_required
def dashboard_posts_edit(request, post_slug):
    current_post = Post.objects.get(slug = post_slug)
    current_category = current_post.category

    if request.method =='POST':
        draft_form = Draft_form(request.POST,prefix='draft',instance=current_post)
        category_form = Category_form(request.POST, prefix='category',instance=current_category)
        if draft_form.is_valid() and category_form.is_valid():
            category_form.save()
            draft_form.save()
            messages.success(request, 'Post edited.',extra_tags="alert alert-success")
            return redirect('sampleblog:dashboard_posts')
    else:
        draft_form = Draft_form(prefix='draft',instance=current_post)
        category_form = Category_form(prefix='category',instance=current_category)

        context ={
        'draft_form':draft_form,
        'category_form':category_form
        }

        return render(request,'sampleblog/dashboard_posts_edit.html',context)

@login_required
def dashboard_posts_delete(request, post_slug):
    current_post = Post.objects.get(slug = post_slug)
    current_post.delete()
    current_post.category.delete()
    messages.success(request, 'Post deleted.',extra_tags="alert alert-success")
    return redirect('sampleblog:dashboard_posts')





@login_required()
def dashboard_comments(request):

        username = request.user.username
        current_user = User.objects.get(username = username)
        current_comments = Comment.objects.filter(user=current_user).order_by('-created_date')
        current_comments_count = current_comments.count()
        if current_comments_count == 0:
            messages.info(request, 'You have no comments. Make one.', extra_tags="alert alert-info")

        paginator = Paginator(current_comments, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_comments_current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_comments_current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_comments_current_page = paginator.page(paginator.num_pages)

        context={
        'current_user':current_user,
        'current_comments_current_page':current_comments_current_page,
        'current_comments_count' :current_comments_count
        }

        return render(request,'sampleblog/dashboard_comments.html',context)


@login_required()
def dashboard_comments_edit(request,comment_slug):
    current_comment = Comment.objects.get(slug = comment_slug)
    # current_category = current_post.category

    if request.method =='POST':
        post_form = Comment_form(request.POST,instance=current_comment)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Comment edited.',extra_tags="alert alert-success")
            return redirect('sampleblog:dashboard_comments')
    else:
        comment_form = Comment_form(instance=current_comment)
        context ={
        'comment_form':comment_form
        }

        return render(request,'sampleblog/dashboard_comments_edit.html',context)

@login_required()
def dashboard_comments_delete(request,comment_slug):

        current_comment = Comment.objects.get(slug = comment_slug)
        current_comment.delete()
        messages.success(request, 'Comment deleted.',extra_tags="alert alert-success")
        return redirect('sampleblog:dashboard_comments')

@login_required()
def dashboard_profile(request):

        username = request.user.username
        current_user = User.objects.get(username = username)
        current_profile = Profile.objects.filter(user=current_user).first()

        if current_profile is None:
            messages.info(request, 'You have no profile. Make one.',extra_tags="alert alert-info")

        context={
        'current_user':current_user,
        'current_profile':current_profile,
        }

        return render(request,'sampleblog/dashboard_profile.html',context)

@login_required()
def dashboard_profile_add(request):

    username = request.user.username
    current_user = User.objects.get(username = username)
    current_profile = Profile.objects.filter(user=current_user).first()

    if request.method == 'POST':
        profile_form = Profile_form(request.POST,request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile added.',extra_tags="alert alert-success")
            return redirect('sampleblog:dashboard_profile')

    else:
        if current_profile is not None:
            messages.info(request, 'Profile already exists.', extra_tags="alert alert-info")
            return redirect('sampleblog:dashboard_profile')
        else:
            profile_form = Profile_form()
            context ={
            'profile_form':profile_form
            }
            return render(request,'sampleblog/dashboard_profile_add.html',context)

@login_required()
def dashboard_profile_edit(request):

    username = request.user.username
    current_user = User.objects.get(username = username)
    current_profile = Profile.objects.filter(user=current_user).first()

    if request.method == 'POST':
        form = Profile_form(request.POST,request.FILES, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile edited.',extra_tags="alert alert-success")
            return redirect('sampleblog:dashboard_profile')
    else:
        if current_profile is None:
            messages.info(request, 'There is no profile to edit.',extra_tags="alert alert-info")
            return redirect('sampleblog:dashboard_profile')

        else:
            profile_form = Profile_form(instance=current_profile)
            context={
            'profile_form':profile_form
            }
            return render(request,'sampleblog/dashboard_profile_edit.html',context)

@login_required()
def dashboard_profile_delete(request):

    username = request.user.username
    current_user = User.objects.get(username = username)
    current_profile = Profile.objects.filter(user=current_user).first()

    if current_profile is None:
        messages.info(request, 'There is no profile to delete.',extra_tags="alert alert-info")
        return redirect('sampleblog:dashboard_profile')

    else:
        current_profile.delete()
        messages.success(request, 'Profile deleted.',extra_tags="alert alert-success")
        return redirect('sampleblog:dashboard_profile')


# def test(request):
#     return render(request,'sampleblog/test.html')

# def add_comment(request):
    # if request.method =='POST':
    #     form = Post_form(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #
    #         comment.user = request.user
    #         comment.save()
    #         # return redirect('/blog/user_profile/')
    # else:
    #     form = Comment_form()

    # context ={
    # 'form':form
    # }
    # return render(request,'sampleblog/post_details.html',context)
