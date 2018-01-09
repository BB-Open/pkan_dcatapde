from zope.component.hooks import getSite


def get_foafagent_context():
    # todo context should not be the site
    context = getSite()
    return context

def get_obj_by_path(choice):
    # TODO
    pass