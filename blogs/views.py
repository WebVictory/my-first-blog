from calendar import month_name

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import timezone
from mezzanine.utils.views import paginate

import myapp
from myapp.models import MyProfile
from myproject import settings
from myproject.settings import ACCOUNTS_PROFILE_MODEL
from .forms import MyBlogForms, BlogPostNewForms
from .models import MyBlog, BlogPostNew
from guardian.shortcuts import assign_perm, get_perms


@login_required
def blog_new(request):
    if request.method == "POST":
        form = MyBlogForms(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.published_date = timezone.now()
            blog.save()
            joe = User.objects.get(username=request.user.username)
            task = MyBlog.objects.get(slug=blog.slug)
            blog.author.add(request.user.myprofile)
            assign_perm('add_myblog', joe, task)
            assign_perm('change_myblog', joe, task)
            assign_perm('delete_myblog', joe, task)
            blog.save()

            return redirect('blog_detail', slug=blog.slug)
    else:
        form = MyBlogForms()
    return render(request, 'pages/blog_edit.html', {'form': form})

@login_required
def blog_edit(request, slug):
    joe = User.objects.get(username=request.user.username)
    blog = get_object_or_404(MyBlog, slug=slug)
    if ('change_myblog' in get_perms(joe, blog)):
    # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = MyBlogForms(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                blog = form.save(commit=False)
                # blog.author = request.user
                # blog.published_date = timezone.now()
                form.save()
                return redirect('blog_detail', slug=blog.slug)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = MyBlogForms(instance=blog)

        return render(request, 'pages/blog_edit.html', {'form': form})

    return redirect('blog_detail', slug=blog.slug)

@login_required
def blog_post_new(request):
    if request.method == "POST":
        form = BlogPostNewForms (request.POST, user_id= request.user.id)
        if form.is_valid():
            save_form = form.save(commit=False)
            # save_form.content = form.cleaned_data.get('content', 'pppp')
            save_form.user = request.user
            save_form.save()
            joe = User.objects.get(username=request.user.username)
            task = BlogPostNew.objects.get(slug=save_form.slug)
            assign_perm('add_blogpostnew', joe, task)
            assign_perm('change_blogpostnew', joe, task)
            assign_perm('delete_blogpostnew', joe, task)
            save_form.save()

            # save_form = form.save()
            return redirect('blog_post_detail', slug=save_form.slug)
    else:
        form = BlogPostNewForms()
    return render(request, 'pages/blog_post_edit.html', {'form': form})




# form = UserLoginForm(request.POST or None)
#     context = { 'form': form, }
#     if request.method == 'POST' and form.is_valid():
#         username = form.cleaned_data.get('username', None)
#         password = form.cleaned_data.get('password', None)
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             return redirect('index_page')
#     return direct_to_template(request, 'form.html', context)

@login_required
def blog_post_edit(request, slug):

    post = get_object_or_404(BlogPostNew, slug=slug)
    joe = User.objects.get(username=request.user.username)
    if ('change_blogpostnew' in get_perms(joe, post)):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = BlogPostNewForms(request.POST, request.FILES, instance=post)
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.user = request.user
                save_form = form.save()
                return redirect('blog_post_detail', slug=save_form.slug)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = BlogPostNewForms(instance=post)
        return render(request, 'pages/blog_post_edit.html', {'form': form})
    return redirect('blog_post_detail', slug=post.slug)

def blog_list(request, tag=None, year=None, month=None, username=None,
              category=None, template="pages/blogs_list.html",
              extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    blog_posts = MyBlog.objects.all()
    # blog_posts = Blog.objects.published(for_user=request.user)
    # if tag is not None:
    #     tag = get_object_or_404(Keyword, slug=tag)
    #     blog_posts = blog_posts.filter(keywords__keyword=tag)
    # if year is not None:
    #     blog_posts = blog_posts.filter(publish_date__year=year)
    #     if month is not None:
    #         blog_posts = blog_posts.filter(publish_date__month=month)
    #         try:
    #             month = _(month_name[int(month)])
    #         except IndexError:
    #             raise Http404()
    # if category is not None:
    #     category = get_object_or_404(BlogCategory, slug=category)
    #     blog_posts = blog_posts.filter(categories=category)
    #     templates.append(u"blog/blog_post_list_%s.html" %
    #                       str(category.slug))
    author = None
    # if username is not None:
    #     author = get_object_or_404(ACCOUNTS_PROFILE_MODEL, username=username)
    #     blog_posts = blog_posts.filter(user=author)
    #     templates.append(u"blog/blog_post_list_%s.html" % username)

    # prefetch = ("categories", "keywords__keyword")
    # blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    context.update(extra_context or {})
    templates.append(template)
    # return TemplateResponse(request, templates, context)
    return render(request, 'pages/blogs_list.html', context)


def blog_detail(request, slug, year=None, month=None, day=None,
                template="pages/blog_detail.html",
                extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    # blog_posts = MyBlog.objects.get(slug=slug)
    blog_post = get_object_or_404(MyBlog, slug=slug)
    par_blog_posts = BlogPostNew.objects.filter(blog=blog_post)
    blog_posts = paginate(par_blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    # related_posts = blog_post.related_posts.published(for_user=request.user)
    context = {"blog_post": blog_post, "editable_obj": blog_post, "blog_posts": blog_posts}
    context.update(extra_context or {})
    templates = [u"pages/blog_detail.html", template]
    # return TemplateResponse(request, templates, context)
    return render(request, 'pages/blog_detail.html', context)


def blog_post_detail(request, slug ):

    blog_post = get_object_or_404(BlogPostNew, slug=slug)
    context = {"blog_post": blog_post}
    return render(request, "blog/blog_post_detail.html", context)

def author_list(request, tag=None, year=None, month=None, username=None,
              category=None, template="pages/blogs_list.html",
              extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    blog_posts = MyProfile.objects.all()
    author = None
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author, }
    context.update(extra_context or {})
    templates.append(template)
    return render(request, 'pages/author_list.html', context)

