import pytest

from pages.models import Page, Video, Text, PageContent


@pytest.mark.django_db
def test_list(client):
    Page.objects.create(title="test")
    response = client.get("/pages/")
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [{"pk": 1, "title": "test", "details_url": "http://testserver/pages/1/"}],
    }


@pytest.mark.django_db
def test_details(client):
    page = Page.objects.create(title="test")
    video = Video.objects.create(
        title="test", video_file_url="http://example.com", subtitles_file_url="http://example.com"
    )
    text = Text.objects.create(title="test", content="test")
    PageContent.objects.create(page=page, content=video)
    PageContent.objects.create(page=page, content=text)
    response = client.get(f"/pages/{page.pk}/")
    assert response.json() == {
        "content": [
            {
                "content": {
                    "counter": 1,
                    "pk": video.pk,
                    "subtitles_file_url": "http://example.com",
                    "title": "test",
                    "video_file_url": "http://example.com",
                },
                "content_type": "Video",
                "order": 0,
            },
            {
                "content": {"content": "test", "counter": 1, "pk": text.pk, "title": "test"},
                "content_type": "Text",
                "order": 0,
            },
        ],
        "pk": page.pk,
        "title": "test",
    }
