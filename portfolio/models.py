from django.db import models

from wagtail.models import Page 
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel 

from portfolio.blocks import PortfolioStreamBlock 
# Create your models here.

class PortfolioPage(Page):
    parent_page_types = ['home.HomePage']

    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True, 
        help_text = 'Use this secton to list you projects.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]
