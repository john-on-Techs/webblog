from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from .models import Post


class PostFeed(Feed):
    title = "Oenga John Blog Feeds"
    link = '/feed/'
    description = 'Latest Posts!'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars_html(item.text, 20)
        # return truncatewords(item.text)
