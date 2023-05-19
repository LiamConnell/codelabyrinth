// ui/src/App.tsx
import React, {useState, CSSProperties } from 'react';
import QueryPanel from './components/QueryPanel';
import LogPanel from './components/LogPanel';
import {Box, Container} from '@mui/material';
import { AppBar, Toolbar, Typography, Switch } from '@mui/material';



const styles = {
  root: {
    // display: 'flex',
    // flexDirection: 'column',
    height: '100vh', // full height of the viewport
    overflow: 'scroll'
    // background: "black",
    // color: "white"
  } as CSSProperties,
  appBar: {
    zIndex: 1400, // Material-UI default drawer zIndex is 1300
    // background: 'rgba(0, 224, 181, 1)'
    // background: 'rgba(110, 118, 250, 1)'
    // background: 'rgba(20, 230, 230, 1)'
    background: 'rgba(43, 11, 158, 1)'
  } as CSSProperties,
  content: {
    flexGrow: 1,
    padding: 16, // theme.spacing(3) equivalent
    // display: 'flex',
    // flexDirection: 'column',
    justifyContent: 'space-between',
  } as CSSProperties,
  main: {
    // height: '60%',
    // overflow: 'scroll',
    // background: 'rgba(43, 11, 158, 1)'
  } as CSSProperties,
  bottom: {
    // height: '30%',
    // overflow: 'hidden',
  } as CSSProperties,
};


function App() {
  const [nightMode, setNightMode] = useState(false);
  const handleNightModeToggle = () => {
    setNightMode(!nightMode);
  };



  return (
      <div style={styles.root}>
      <AppBar position="fixed" style={styles.appBar}>
        <Toolbar>
          <Typography variant="h6" noWrap>
            Code Labyrinth
          </Typography>
          {/*<Switch checked={nightMode} onChange={handleNightModeToggle} />*/}
          {/*<Typography variant="body1" noWrap>Night Mode</Typography>*/}
        </Toolbar>
      </AppBar>
      <Toolbar /> {/* This toolbar acts as a spacer */}

      <main style={styles.content}>
        <div style={styles.main}>
          {/* Add your main content here */}
          <LogPanel />
        </div>
        <div style={styles.bottom}>
          <QueryPanel />
        </div>
      </main>
    </div>
  );
}

export default App;
