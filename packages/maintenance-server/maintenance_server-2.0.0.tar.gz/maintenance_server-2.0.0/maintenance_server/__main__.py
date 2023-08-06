from . import maintenance_server

if __name__ == "__main__":
    config = maintenance_server.ServerConfig.get_config()
    print("Start a process on ", config)
    maintenance_server.get_server(config).serve_forever()
