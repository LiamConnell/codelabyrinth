// ui/src/components/QueryPanel.tsx
import React, { useState } from 'react';
import CollectionsList from './CollectionsList';
import QuestionEntry from './QuestionEntry';
import AgentsList from './AgentsList';
import { Grid, Paper } from '@mui/material';

const QueryPanel = () => {
  const [selectedCollections, setSelectedCollections] = useState<string[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>('');

  const handleCollectionSelect = (collections: string[]) => {
    setSelectedCollections(collections);
  };

  const handleSubmit = (question: string) => {
    fetch('http://localhost:8000/code/qa', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        collections: selectedCollections,
        question: question,
        agent: selectedAgent, // Add the selected agent to the request body
      }),
    });
  };

  return (
    <Paper

      sx={{
          elevation: 5,
        position: 'fixed',
        // top: 50,
        marginTop: "10px",
           marginBottom: "5px",
           marginLeft: "5px",
           marginRight: "5px",
        bottom: 0,
        left: 0,
        right: 0,
        height: '25%',
        // padding: "10px",
        background: 'rgba(110, 118, 250, .2)',
        overflow: "scroll",
          // flex: 'auto'
      }}
    >
      <Grid container spacing={2}>
        <Grid item xs={2}>
          <CollectionsList onCollectionSelect={handleCollectionSelect} />
        </Grid>
        <Grid item xs={2}>
          <AgentsList onAgentSelect={setSelectedAgent} />
        </Grid>
        <Grid item xs={8}>
          <QuestionEntry onSubmit={handleSubmit} />
        </Grid>
      </Grid>
    </Paper>
  );
};

export default QueryPanel;
