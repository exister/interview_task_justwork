from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin

from pages.models import Page, Video, Audio, Text, Content, PageContent


class BaseContentAdmin(PolymorphicChildModelAdmin):
    base_model = Content


@admin.register(Video)
class VideoAdmin(BaseContentAdmin):
    base_model = Video


@admin.register(Audio)
class AudioAdmin(BaseContentAdmin):
    base_model = Audio


@admin.register(Text)
class TextAdmin(BaseContentAdmin):
    base_model = Text


@admin.register(Content)
class ContentAdmin(PolymorphicParentModelAdmin):
    base_model = Content
    child_models = (Video, Audio, Text)


class ContentInline(SortableInlineAdminMixin, admin.StackedInline):
    model = PageContent
    extra = 1
    raw_id_fields = ("content",)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ("^title", "^content__title")
    inlines = (ContentInline,)
