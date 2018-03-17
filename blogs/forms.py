from django.forms import ModelForm

from blogs.models import MyBlog, BlogPostNew
from myapp.models import MyProfile
from django.contrib.auth.models import User

class MyBlogForms(ModelForm):
    class Meta:
        model = MyBlog
        fields = '__all__'
        # fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ['author']


class BlogPostNewForms(ModelForm):
    class Meta:
        model = BlogPostNew
        fields = '__all__'
        exclude =['user','related_posts','featured_image', 'publish_date', 'short_description','slug','short_url','_meta_title','expiry_date','gen_description','in_sitemap','keywords','categories', 'description']

    # def __init__(self, *args, **kwargs):
    #     super(BlogPostNewForms, self).__init__(*args, **kwargs)
    #     self.queryset = MyBlog.objects.filter(name='myblog')
    def __init__(self, user_id=None, *args, **kwargs):
        super(BlogPostNewForms, self).__init__(*args, **kwargs)
        if self.instance:
            # self.fields['blog'].queryset = MyBlog.objects.filter(name='myblog')
            self.fields['blog'].queryset = MyBlog.objects.filter(author=user_id)

