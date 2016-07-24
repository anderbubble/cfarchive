def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('swarm_peers', '/swarm/peers')

    config.add_route('new_object', '/objects/new')
    config.add_route('list_objects', '/objects', request_method='GET')
    config.add_route('create_object', '/objects', request_method='POST')
    config.add_route('retrieve_object', '/objects{id_:/ipfs/[^/]+}', request_method='GET')
