from Acquisition import aq_inner
from five import grok
from plone import api

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.contentlisting.interfaces import IContentListing

from twt.events.bookableevent import IBookableEvent

from twt.events import MessageFactory as _


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
