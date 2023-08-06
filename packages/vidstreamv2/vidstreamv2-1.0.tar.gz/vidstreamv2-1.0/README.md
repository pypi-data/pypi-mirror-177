# vidstreamV2

Based on vidsteam!

Developed by 
## Examples of How To Use ( Has some bugs)

Creating A Server

```python
from vidstreamv2 import StreamingServer

server = StreamingServer('127.0.0.1', 9999)
server.start_server()

# Other Code

# When You Are Done
server.stop_server()
```

Creating A Client
```python
from vidstreamv2 import CameraClient
from vidstreamv2 import VideoClient
from vidstreamv2 import ScreenShareClient

# Choose One
client1 = CameraClient('127.0.0.1', 9999)
client2 = VideoClient('127.0.0.1', 9999, 'video.mp4')
client3 = ScreenShareClient('127.0.0.1', 9999)

client1.start_stream()
client2.start_stream()
client3.start_stream()
```