from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Category,Country,Language,Link, Tag

class LatestLinksFeed(Feed):
    title = "Police beat site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to police beat central."

    def items(self):
        return Link.objects.order_by('-added')[:100]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
    def item_photo(self,item):
        return item.image_file.url
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('links', args=[item.linkId])