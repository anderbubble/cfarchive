from pyramid.view import view_config


@view_config(route_name='swarm_peers', renderer='json')
def swarm_peers (request):
    pass #return {'peers': ipfsApi.swarm.peers()}
