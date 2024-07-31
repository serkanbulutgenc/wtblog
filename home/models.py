from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField 


class HomePage(Page):
    body = RichTextField(blank=True, help_text="Body field for Home page")


    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]