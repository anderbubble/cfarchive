def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('swarm_peers', '/swarm/peers')
    config.add_route('upload', '/upload')
