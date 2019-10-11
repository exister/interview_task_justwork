from rest_framework import serializers, reverse

from .models import Page, Content, Video, Audio, Text, PageContent


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('pk', 'title', 'counter')


class VideoSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        model = Video
        fields = ContentSerializer.Meta.fields + ('video_file_url', 'subtitles_file_url')


class AudioSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        model = Audio
        fields = ContentSerializer.Meta.fields + ('audio_file_url', 'bitrate')


class TextSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        model = Text
        fields = ContentSerializer.Meta.fields + ('content',)


CONTENT_SERIALIZERS = {
    Video: VideoSerializer,
    Audio: AudioSerializer,
    Text: TextSerializer,
}


class PageContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = PageContent
        fields = ('content', 'content_type', 'order')

    def get_content(self, obj):
        return CONTENT_SERIALIZERS.get(type(obj.content), ContentSerializer)(obj.content).data

    def get_content_type(self, obj):
        return obj.content.__class__.__name__


class BasePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('pk', 'title',)


class PageListItemSerializer(BasePageSerializer):
    details_url = serializers.SerializerMethodField()

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + ('details_url',)

    def get_details_url(self, obj):
        return reverse.reverse('page-detail', args=(obj.pk,), request=self.context['request'])


class PageDetailsSerializer(BasePageSerializer):
    content = PageContentSerializer(source='pagecontent_set', many=True)

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + ('content',)
