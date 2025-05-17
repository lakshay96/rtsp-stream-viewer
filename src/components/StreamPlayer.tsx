import React, { useEffect, useRef, useState } from 'react';
import { Card, CardMedia, CardContent, CardActions, Button, Typography } from '@mui/material';

type StreamPlayerProps = {
  streamId: number;
  url: string;
  wsBaseUrl: string;
  onRemove: () => void;
};

const StreamPlayer: React.FC<StreamPlayerProps> = ({ streamId, url, wsBaseUrl, onRemove }) => {
  const [paused, setPaused] = useState(false);
  const [frameSrc, setFrameSrc] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  // Open WebSocket connection on mount and set up message handlers
  useEffect(() => {
    const wsUrl = `${wsBaseUrl.replace('http', 'ws')}/ws/streams/${streamId}/`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log(`WebSocket connected for stream ${streamId}`);
      setError(null);
    };
    socket.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.frame) {
          // Update image source if not paused
          if (!paused) {
            setFrameSrc(`data:image/jpeg;base64,${msg.frame}`);
          }
        } else if (msg.error) {
          // Handle error message from server
          console.error("Stream error:", msg.error);
          setError(msg.error);
          // Optionally, close socket on error (no more frames expected)
          socket.close();
        }
      } catch (err) {
        console.error("Failed to parse WS message", err);
      }
    };
    socket.onclose = () => {
      console.log(`WebSocket disconnected for stream ${streamId}`);
    };
    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
      setError("WebSocket error");
    };

    // Cleanup on unmount: close socket
    return () => {
      socket.close();
    };
  }, [streamId, wsBaseUrl, paused]);

  // Toggle pause state
  const handleTogglePause = () => {
    setPaused(prev => !prev);
    // If we wanted to truly stop streaming on pause, we could send a message or close the socket here.
    // In this implementation, pause simply freezes the video on the last frame.
  };

  return (
    <Card>
      {/* Display the video frame or a placeholder if no frame yet */}
      <CardMedia 
        component="img" 
        image={frameSrc || "https://via.placeholder.com/400?text=No+Stream"} 
        alt="Stream video" 
      />
      <CardContent>
        {error ? (
          <Typography color="error" variant="body2">
            {error}
          </Typography>
        ) : (
          <Typography variant="body2" color="textSecondary">
            {url}
          </Typography>
        )}
      </CardContent>
      <CardActions>
        <Button size="small" onClick={handleTogglePause}>
          {paused ? "Play" : "Pause"}
        </Button>
        <Button size="small" color="error" onClick={onRemove}>
          Remove
        </Button>
      </CardActions>
    </Card>
  );
};

export default StreamPlayer;
