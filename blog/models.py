from django.db import models
from django import forms
'''
MyModel.objects.descendant_of(somepage)
child_of(page) / not_child_of(somepage)
ancestor_of(somepage) / not_ancestor_of(somepage)
parent_of(somepage) / not_parent_of(somepage) 
sibling_of(somepage) / not_sibling_of(somepage) / 

somepage.get_children()
somepage.get_ancestors()
somepage.get_descendants()
somepage.get_siblings()

'''

from modelcluster.models import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField 
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request, *args, **kwargs):
        ctx =super().get_context(request, *args, **kwargs)
        blogpages = self.get_children().live().order_by('-first_published_at')
        ctx["blogpages"] = blogpages
        return ctx

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    date = models.DateField("Post Date")
    intro = models.CharField(max_length=200)
    body= RichTextField(blank=True)

    authors = ParentalManyToManyField('blog.Author', blank=True)

    tags =  ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()

        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields +[
        index.SearchField('intro'),
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags')
        ], heading="Blog Information"),
        FieldPanel('intro'),
        FieldPanel('body'),

        InlinePanel('gallery_images', label='Gallery Images')
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption=models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption')
    ]

class BlogTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        
        ctx = super().get_context(request, *args, **kwargs)
        ctx['blogpages'] =blogpages
        return ctx


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey('wagtailimages.image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image')
    ]

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural = 'Authors'