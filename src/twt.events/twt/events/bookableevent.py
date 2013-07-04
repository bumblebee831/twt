import datetime
from DateTime import DateTime
from five import grok
from zope import schema

from plone.indexer import indexer

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from twt.events import MessageFactory as _


class IBookableEvent(form.Schema, IImageScaleTraversable):
    """
    Bookable event type
    """
    start = schema.Datetime(
        title=_(u"Event Date"),
        required=True,
    )
    location = schema.TextLine(
        title=_(u"Event Location"),
        required=True,
    )
    
    notbookable = schema.Bool(
        title=_(u"Notbookable?"),
        description=_(u"Mark this event as notbookable and a notbooking link will "
                      u"be auto-generated"),
        default=True,
        required=False,
    )

    bookable = schema.Bool(
        title=_(u"Bookable?"),
        description=_(u"Mark this event as bookable and a booking link will "
                      u"be auto-generated"),
        default=True,
        required=False,
    )

    soldout = schema.Bool(
        title=_(u"Sold out"),
        required=False,
    )


@form.default_value(field=IBookableEvent['start'])
def startDefaultValue(data):
    return datetime.datetime.today() + datetime.timedelta(7)


@indexer(IBookableEvent)
def startIndexer(obj):
    if obj.start is None:
        return None
    return DateTime(obj.start.isoformat())
grok.global_adapter(startIndexer, name="start")


class BookableEvent(Container):
    grok.implements(IBookableEvent)


class View(grok.View):
    """ Bookable event view """

    grok.context(IBookableEvent)
    grok.require('zope2.View')
    grok.name('view')
