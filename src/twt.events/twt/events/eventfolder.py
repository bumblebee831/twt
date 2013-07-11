from Acquisition import aq_inner
from five import grok
from plone import api

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.contentlisting.interfaces import IContentListing

from twt.events.bookableevent import IBookableEvent


class IEventFolder(form.Schema, IImageScaleTraversable):
    """
    AEvent collection folder
    """


class EventFolder(Container):
    grok.implements(IEventFolder)


class View(grok.View):
    """ Event listing """

    grok.context(IEventFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_events = len(self.contained_events()) > 0

    def contained_events(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name="portal_catalog")
        items = catalog(object_provides=IBookableEvent.__identifier__,
                        path=dict(query='/'.join(context.getPhysicalPath()),
                                  depth=1),
                        sort_on='start',
                        review_state='published')
        return IContentListing(items)

    def generate_booking_link(self, item):
        portal_url = api.portal.get().absolute_url()
        obj = item.getObject()
        title = obj.title
        start = obj.start
        datestamp = api.portal.get_localized_time(datetime=start)
        timestamp = api.portal.get_localized_time(datetime=start, time_only=True)
        title_param = '?veranstaltungstitel=' + title
        time_param = '&veranstaltungsdatum=' + datestamp + ' ' + timestamp
        base_url = portal_url + '/karten'
        url = base_url + title_param + time_param
        return url

    def format_time(self, time):
        util = api.portal.get_tool(name="translation_service")
        # zope_time = DateTime(time.isoformat())
        return util.toLocalizedTime(time, long_format=True)
