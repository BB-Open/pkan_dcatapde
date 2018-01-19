from Acquisition import IAcquirer
from Acquisition import aq_base
from Acquisition import aq_inner

from Acquisition.interfaces import IAcquirer
from plone.dexterity.browser import add
from plone.dexterity.interfaces import IDexterityFTI
from z3c.form import form
from zope.component import createObject
from zope.component import getUtility


class PkanDefaulftAddForm(add.DefaultAddForm):

    def create(self, data):
        fti = getUtility(IDexterityFTI, name=self.portal_type)

        container = aq_inner(self.context)

        # give data to factory, so it can make checks
        content = createObject(fti.factory, **data)

        # Note: The factory may have done this already, but we want to be sure
        # that the created type has the right portal type. It is possible
        # to re-define a type through the web that uses the factory from an
        # existing type, but wants a unique portal_type!

        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())

        # Acquisition wrap temporarily to satisfy things like vocabularies
        # depending on tools
        if IAcquirer.providedBy(content):
            content = content.__of__(container)

        form.applyChanges(self, content, data)
        for group in self.groups:
            form.applyChanges(group, content, data)

        return aq_base(content)




class PkanDefaultAddView(add.DefaultAddView):
    form = PkanDefaulftAddForm