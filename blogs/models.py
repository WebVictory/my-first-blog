from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext
from mezzanine.blog.models import BlogPost
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Slugged
from mezzanine.utils.models import base_concrete_model
from mezzanine.utils.urls import unique_slug, slugify
from django.utils.translation import ugettext, ugettext_lazy as _
from myproject.settings import ACCOUNTS_PROFILE_MODEL


class MyBlog(models.Model):
    name = models.CharField(max_length=200)
    description =models.TextField(blank=True)
    author = models.ManyToManyField(ACCOUNTS_PROFILE_MODEL)
    publish_date = models.DateField(auto_now=True, blank=True)
    avatar = models.ImageField(upload_to='uploads/', default='uploads\gallery\Berlin, Germany.jpg', blank=True)
    slug = models.CharField(max_length=2000, blank=True, null=True,
                            help_text="Leave blank to have the URL auto-generated from "
                                        "the title.")

    def get_absolute_url(self):

        url_name = "blog_detail"
        kwargs = {"slug": self.slug}
        return reverse(url_name, kwargs=kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        permissions = (
            ('view_myblog', 'View myblog'),
        )




    def save(self, *args, **kwargs):
        """
        If no slug is provided, generates one before saving.
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(MyBlog, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Create a unique slug by passing the result of get_slug() to
        utils.urls.unique_slug, which appends an index if necessary.
        """
        # For custom content types, use the ``Page`` instance for
        # slug lookup.
        concrete_model = base_concrete_model(Slugged, self)
        slug_qs = concrete_model.objects.exclude(id=self.id)
        return unique_slug(slug_qs, "slug", self.get_slug())

    def get_slug(self):
        """
        Allows subclasses to implement their own slug creation logic.
        """
        attr = "name"
        # Get self.title_xx where xx is the default language, if any.
        # Get self.title otherwise.
        return slugify(getattr(self, attr, None) or self.name)

    def admin_link(self):
        return "<a href='%s'>%s</a>" % (self.get_absolute_url(),
                                        ugettext("View on site"))

    admin_link.allow_tags = True
    admin_link.short_description = ""


class BlogPostNew(BlogPost):
    blog = models.ForeignKey(MyBlog, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

