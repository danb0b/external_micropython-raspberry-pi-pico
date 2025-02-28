from microdot import Microdot, Response, send_file
from microdot.utemplate import Template
from microdot.websocket import with_websocket
from ldr_photoresistor_module import LDR
import time

# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'

# LDR module
ldr = LDR(27)

# root route
@app.route('/')
async def index(request):
    return Template('index.html').render()


@app.route('/ws')
@with_websocket
async def read_sensor(request, ws):
    while True:
#         data = await ws.receive()
        time.sleep(.1)
        try:
            await ws.send(str(ldr.get_light_percentage()))
        except ConnectionResetError:
            print("connection lost")

# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


# shutdown
@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        pass
