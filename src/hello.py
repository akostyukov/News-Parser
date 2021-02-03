from http.server import HTTPServer

server = HTTPServer(('', 1337), None)
print('Сервер запущен')
server.serve_forever()
