import React, { useState } from 'react';
import { TextField, Button, Grid, Container, Stack } from '@mui/material';
import StreamPlayer from './components/StreamPlayer';

interface StreamInfo {
  id: number;
  url: string;
}

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";  // Backend API
const WS_BASE_URL = process.env.REACT_APP_WS_BASE_URL || "ws://localhost:8000";      // WebSocket base URL

function App() {
  const [streams, setStreams] = useState<StreamInfo[]>([]);
  const [newUrl, setNewUrl] = useState("");

  // Add a new stream by calling backend API
  const handleAddStream = async () => {
    if (!newUrl.trim()) return;
    try {
      const response = await fetch(`${API_BASE_URL}/api/streams/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: newUrl.trim() })
      });
      const data = await response.json();
      if (response.ok) {
        const streamId = data.id;
        setStreams(prev => [...prev, { id: streamId, url: newUrl.trim() }]);
        setNewUrl("");  // clear input field
      } else {
        alert(`Failed to add stream: ${data.error || 'Unknown error'}`);
      }
    } catch (err) {
      console.error("Error adding stream:", err);
      alert("Could not add stream (network error).");
    }
  };

  // Remove stream from state (will unmount StreamPlayer and close its connection)
  const handleRemoveStream = (id: number) => {
    setStreams(prev => prev.filter(s => s.id !== id));
  };

  return (
    <Container sx={{ py: 4 }}>
      {/* Input form to add a new RTSP stream URL */}
      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <TextField 
          label="RTSP Stream URL" 
          variant="outlined" 
          value={newUrl}
          onChange={(e) => setNewUrl(e.target.value)}
          fullWidth
        />
        <Button variant="contained" onClick={handleAddStream}>
          Add Stream
        </Button>
      </Stack>

      {/* Grid layout for multiple streams */}
      <Grid container spacing={2}>
        {streams.map(stream => (
          <Grid item xs={12} sm={6} md={4} key={stream.id}>
            <StreamPlayer 
              streamId={stream.id} 
              url={stream.url} 
              wsBaseUrl={WS_BASE_URL}
              onRemove={() => handleRemoveStream(stream.id)} 
            />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App;
