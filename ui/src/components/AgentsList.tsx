// ui/src/components/AgentsList.tsx
import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

const AgentsList = ({ onAgentSelect }: { onAgentSelect: (agent: string) => void }) => {
  const [agents, setAgents] = useState<string[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>('');

  useEffect(() => {
    fetch('http://localhost:8000/agents')
      .then((response) => response.json())
      .then((data) => setAgents(data));
  }, []);

  const handleAgentClick = (agent: string) => {
    setSelectedAgent(agent);
    onAgentSelect(agent);
  };

  return (
    <>
      <h2>Agents</h2>
      <List>
        {agents.map((agent) => (
          <ListItem
            key={agent}
            button
            onClick={() => handleAgentClick(agent)}
            selected={selectedAgent === agent}
          >
            <ListItemText primary={agent} />
          </ListItem>
        ))}
      </List>
    </>
  );
};

export default AgentsList;
