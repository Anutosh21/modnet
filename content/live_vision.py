"""Camera/display UI. The notebook supplies the Python prediction function."""

import asyncio
import base64
import json
from pathlib import Path
import secrets

import pyjs
from IPython.display import IFrame, display


class LiveVision:
    def __init__(self, predict, *, sample, size, device):
        self.predict = predict
        self.closed = False
        self.tasks = set()
        self.history = []
        self.busy = False
        name = 'live-vision-' + secrets.token_hex(12)
        callback, self.callback_owner = pyjs.create_callable(self._receive)
        self.channel = pyjs.js.eval('''(name, callback) => {
            const channel = new BroadcastChannel(name);
            channel.onmessage = ({data}) => callback(JSON.stringify(data));
            return {
                postMessage: message => channel.postMessage(message),
                close: () => {channel.onmessage = null; channel.close();}
            };
        }''')(name, callback)
        payload = dict(channel=name, size=size, device=device,
                       sample=base64.b64encode(Path(sample).read_bytes()).decode())
        source = Path(__file__).with_name('live_vision.html').read_text()
        source = source.replace('__VISION_PAYLOAD__', json.dumps(payload))
        self.url = str(pyjs.js.eval(
            "html => URL.createObjectURL(new Blob([html], {type:'text/html'}))")(source))
        display(IFrame(self.url, width='100%', height=900,
                       extras=['allow="camera"', 'title="Live portrait matting"',
                               'style="border:0;border-radius:12px"']))

    def _receive(self, text):
        if self.closed:
            return
        request = json.loads(str(text))
        if request.get('kind') != 'frame':
            return
        if self.busy:
            self._send(dict(kind='result', id=request.get('id'), error='A frame is already running.'))
            return
        self.busy = True
        task = asyncio.create_task(self._respond(request))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    def _send(self, response):
        if not self.closed:
            self.channel.postMessage(pyjs.js.JSON.parse(json.dumps(response)))

    async def _respond(self, request):
        try:
            encoded = request.get('jpeg', '')
            if not isinstance(encoded, str) or len(encoded) > 2_000_000:
                raise ValueError('Expected a JPEG frame no larger than 2 MB.')
            jpeg = base64.b64decode(encoded, validate=True)
            response = await self.predict(jpeg, request.get('effect', 'blur'))
            self.history.append(dict(response['timings'], effect=request.get('effect')))
            del self.history[:-120]
            self._send(dict(response, kind='result', id=request['id']))
        except Exception as error:
            self._send(dict(kind='result', id=request.get('id'), error=str(error)))
        finally:
            self.busy = False

    async def close(self):
        if self.closed:
            return
        self._send(dict(kind='closed'))
        self.closed = True
        if self.tasks:
            await asyncio.gather(*tuple(self.tasks), return_exceptions=True)
        self.channel.close()
        self.callback_owner.delete()
        pyjs.js.URL.revokeObjectURL(self.url)
