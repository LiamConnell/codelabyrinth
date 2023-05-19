// ui/src/components/SidePanel.tsx
import React, { useState, useEffect } from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, FormControl, InputLabel, Select, MenuItem, TextField, CircularProgress } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';


const AddCollectionButton = () => {
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  const [inputValues, setInputValues] = useState({ path: '', collectionName: '', baseUrl: '', repoUrl: '' });
  const [loading, setLoading] = useState(false);

  const handleAddSubmit = () => {
    setLoading(true);
    let apiUrl = '';
    let body = {};

    if (selectedOption === 'codebase') {
      apiUrl = 'http://localhost:8000/ingest/directory';
      body = { path: inputValues.path, collection_name: inputValues.collectionName };
    } else if (selectedOption === 'docs') {
      apiUrl = 'http://localhost:8000/ingest/website';
      body = { url: inputValues.baseUrl, collection_name: inputValues.collectionName };
    } else if (selectedOption === 'github') {
      apiUrl = 'http://localhost:8000/ingest/website';
      body = { repo_url: inputValues.repoUrl, collection_name: inputValues.collectionName };
    }

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response data as needed
        setLoading(false);
        setAddDialogOpen(false);
      });
  };



  return (<>
        <Button
        variant="contained"
        color="primary"
        startIcon={<AddIcon />}
        onClick={() => setAddDialogOpen(true)}
      >
        Add Collection
      </Button>
      <Dialog open={addDialogOpen} onClose={() => setAddDialogOpen(false)}>
        <DialogTitle>Add Collection</DialogTitle>
        <DialogContent>
          <FormControl fullWidth>
            <InputLabel>Type</InputLabel>
            <Select
              value={selectedOption}
              onChange={(e) => setSelectedOption(e.target.value)}
            >
              <MenuItem value="codebase">Add codebase collection</MenuItem>
              <MenuItem value="docs">Add docs collection</MenuItem>
              <MenuItem value="github">Add GitHub collection</MenuItem>
            </Select>
          </FormControl>
          {selectedOption === 'codebase' && (
            <>
              <TextField
                label="Path"
                value={inputValues.path}
                onChange={(e) => setInputValues({ ...inputValues, path: e.target.value })}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Collection Name"
                value={inputValues.collectionName}
                onChange={(e) => setInputValues({ ...inputValues, collectionName: e.target.value })}
                fullWidth
                margin="normal"
              />
            </>
          )}
          {selectedOption === 'docs' && (
            <>
              <TextField
                label="Base URL"
                value={inputValues.baseUrl}
                onChange={(e) => setInputValues({ ...inputValues, baseUrl: e.target.value })}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Collection Name"
                value={inputValues.collectionName}
                onChange={(e) => setInputValues({ ...inputValues, collectionName: e.target.value })}
                fullWidth
                margin="normal"
              />
            </>
          )}
          {selectedOption === 'github' && (
            <>
              <TextField
                label="Repo URL"
                value={inputValues.repoUrl}
                onChange={(e) => setInputValues({ ...inputValues, repoUrl: e.target.value })}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Collection Name"
                value={inputValues.collectionName}
                onChange={(e) => setInputValues({ ...inputValues, collectionName: e.target.value })}
                fullWidth
                margin="normal"
              />
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddDialogOpen(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleAddSubmit} color="primary" disabled={loading}>
            {loading ? <CircularProgress size={24} /> : 'Submit'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default AddCollectionButton;
