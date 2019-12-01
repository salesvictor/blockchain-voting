import xmlrpc.server


server = xmlrpc.server.SimpleXMLRPCServer(RPC_SERVER_ADDR)
server.register_introspection_functions()
server.serve_forever()
