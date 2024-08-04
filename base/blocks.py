from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock, 
    StructBlock
)

from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution =  CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'base/blocks/image_block.html'

class HeadingBlock(StructBlock):
    heading_text=CharBlock(classname='title', required=True)
    size = ChoiceBlock(
        choices=[
            ('', 'Selec a heading size'),
            ('h2', 'H2'),
            ('h3', 'H3'), 
            ('h4', 'H4')
        ],
        blank=True,
        required=False 
    )

    class Meta:
        icon='title'
        template = 'base/blocks/heading_block.html'

class BaseStreamBlock(StreamBlock):
    HeadingBlock = HeadingBlock()
    paragraph_block= RichTextBlock(icon='pilcrow')
    image_block = ImageBlock()
    embed_block = EmbedBlock(
        help_text='Insert a URL to embed.',
        icon='media'
    )