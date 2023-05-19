// ui/src/components/LogPanel.tsx
import React, { useEffect, useState, useRef } from 'react';
import { List, ListItem, ListItemText, Paper, Grid, Box } from '@mui/material';
import MarkdownPreview from '@uiw/react-markdown-preview';
import { Snackbar } from '@mui/material';
import Alert from '@mui/material/Alert';

interface Log {
  timestamp: string;
  name: string;
  dirname: string
}

const LogPanel = () => {
  const [logs, setLogs] = useState<Log[]>([]);
  const [selectedLog, setSelectedLog] = useState<string>('');
  const [markdownDocs, setMarkdownDocs] = useState<{ prompt: string; response: string }>({ prompt: '', response: '' });
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
  const logsRef = useRef(logs); // Add this ref to store the latest value of logs

  useEffect(() => {
    logsRef.current = logs; // Update the ref value whenever logs change
  }, [logs]);

  useEffect(() => {
    const fetchLogs = () => {
      fetch('http://localhost:8000/logs')
        .then((response) => response.json())
        .then((data) => {
          console.log(logsRef.current.length, data.logs.length); // Use logsRef.current instead of logs
          if (logsRef.current.length > 0 && data.logs.length > logsRef.current.length) {
            setSnackbarOpen(true);
          }
          setLogs(data.logs);
        });
    };

    fetchLogs(); // Fetch logs initially

    const intervalId = setInterval(fetchLogs, 5000); // Set up the interval to fetch new logs every 5 seconds

    return () => {
      clearInterval(intervalId); // Clean up the interval when the component is unmounted
    };
  }, []);

  const handleCloseSnackbar = () => {
      setSnackbarOpen(false);
  };


  const handleLogSelect = (logName: string) => {
    setSelectedLog(logName);
    fetch(`http://localhost:8000/logs/${logName}`)
      .then((response) => response.json())
      .then((data) => setMarkdownDocs({ prompt: data.prompt, response: data.response }));
  };

    return (
        <>
    <div
        style={{
          position: 'fixed',
          top: 64,
          left: 0,
          right: 0,
          height: 'calc(75% - 88px)',
          //   bottom: '25%',
          padding: 2,
            marginLeft: '10px',
            marginRight: '10px',
            marginTop: '10px',
            // marginLeft: '10px'
            overflow: 'hidden'
        }}
      >
        <Grid container spacing={2} height={.93}>
          <Grid item xs={2} height="1">
            <h1>Logs</h1>
            <Box
              sx={{
                height: '100%',
                overflowY: 'scroll',
                paddingRight: 1,
                borderRight: '1px solid rgba(0, 0, 0, 0.12)',
              }}
            >
              <List>
                {logs.map((log) => (
                  <ListItem button key={log.name} onClick={() => handleLogSelect(log.dirname)}>
                    <ListItemText primary={`${log.timestamp} - ${log.name}`} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Grid>
          <Grid item xs={10} height="1">
            <Grid container spacing={0} height="1">
              <Grid item xs={6} height="1">
                <h2>Prompt</h2>
                <Box
                  sx={{
                    height: '100%',
                    overflowY: 'scroll',
                    paddingRight: 1,
                    borderRight: '1px solid rgba(0, 0, 0, 0.12)',
                  }}
                >
                  <MarkdownPreview source={markdownDocs.prompt} wrapperElement={{"data-color-mode": "light"}}/>
                </Box>
              </Grid>
              <Grid item xs={6} height="1">
                <h2>Response</h2>
                <Box
                  sx={{
                    height: '100%',
                    overflowY: 'auto',
                    paddingLeft: 1,
                  }}
                >
                  <MarkdownPreview source={markdownDocs.response} wrapperElement={{"data-color-mode": "light"}} />
                </Box>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>
    <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
    >
        <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
            {`New log available: ${logs.at(-1)}`}
        </Alert>
    </Snackbar>
    </>
  );
};

export default LogPanel;
