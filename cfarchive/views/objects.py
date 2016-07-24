from pyramid.view import view_config

import pyramid.httpexceptions

from ..models import Object


@view_config(route_name='new_object', renderer='../templates/new-object.jinja2')
def upload (request):
    return {}


@view_config(route_name='list_objects', request_method='GET', renderer='../templates/object-list.jinja2')
def list_objects (request):
    objects = list(request.dbsession.query(Object))
    return {'objects': objects}


@view_config(route_name='create_object', request_method='POST', renderer='json')
def create_object (request):
    file_name = request.params['file'].filename
    object_ = Object.from_file(
        request.params['file'].file,
        file_name=request.params['file'].filename,
        content_type=request.params['file'].headers['Content-Type'],
        dbsession=request.dbsession)
    request.dbsession.add(object_)
    request.dbsession.flush()
    raise pyramid.httpexceptions.HTTPFound(
        request.route_url('retrieve_object', id_=object_.id_))


@view_config(route_name='retrieve_object', request_method='GET', renderer='json')
def retrieve_object (request):
    object_ = request.dbsession.query(Object).filter_by(id_=request.matchdict['id_']).one()
    return {'object': object_}
