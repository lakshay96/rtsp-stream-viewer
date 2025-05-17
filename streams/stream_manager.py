import threading
import cv2
import base64
import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

streams = {}
next_id = 1
streams_lock = threading.Lock()

def add_stream(url: str) -> int:
    global next_id
    with streams_lock:
        stream_id = next_id
        next_id += 1
    stop_event = threading.Event()
    streams[stream_id] = {
        'url': url,
        'thread': None,
        'stop_event': stop_event,
        'clients': 0
    }
    return stream_id

def start_stream(stream_id: int):
    stream_info = streams.get(stream_id)
    if stream_info and stream_info['thread'] is None:
        thread = threading.Thread(target=_stream_video, args=(stream_id,))
        thread.daemon = True
        stream_info['thread'] = thread
        thread.start()

def stop_stream(stream_id: int):
    stream_info = streams.get(stream_id)
    if not stream_info:
        return
    stop_event = stream_info['stop_event']
    stop_event.set()
    if stream_info['thread']:
        stream_info['thread'].join(timeout=5)
        stream_info['thread'] = None
    stop_event.clear()

def _stream_video(stream_id: int):
    stream_info = streams.get(stream_id)
    if not stream_info:
        return

    url = stream_info['url']
    stop_event = stream_info['stop_event']
    group_name = f"stream_{stream_id}"
    channel_layer = get_channel_layer()

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|stimeout;5000000"
    cap = cv2.VideoCapture(0)

    video_path = r"/Users/lakshayaggarwal/Desktop/Skylark labs/sample.mp4"
    print("File exists:", os.path.exists(video_path))  # Should print True
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "frame_message", "error": "Failed to connect to stream"}
        )
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            continue
        b64_str = base64.b64encode(buffer).decode('utf-8')
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "frame_message", "frame": b64_str}
        )
        if stop_event.wait(0.1):
            break

    cap.release()
    if not stop_event.is_set():
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "frame_message", "error": "Stream ended or connection lost"}
        )
    if stream_id in streams:
        streams[stream_id]['thread'] = None