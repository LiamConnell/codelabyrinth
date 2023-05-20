import React, { useState, useEffect } from 'react';
import RefreshIcon from '@mui/icons-material/Refresh';
import DeleteIcon from '@mui/icons-material/Delete';
import {
  IconButton,
  Button,
  List,
  ListItem,
  DialogContentText,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Box
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import AddCollectionButton from "./AddCollectionButton";


const CollectionsList = ({ onCollectionSelect }: { onCollectionSelect: (collections: string[]) => void }) => {
  const [collections, setCollections] = useState<string[]>([]);
  const [selectedCollections, setSelectedCollections] = useState<string[]>([]);

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [collectionToDelete, setCollectionToDelete] = useState('');

  const openDeleteDialog = (collection: string) => {
    setCollectionToDelete(collection);
    setDeleteDialogOpen(true);
  };

  useEffect(() => {
    fetch('http://localhost:8000/collections')
      .then((response) => response.json())
      .then((data) => setCollections(data));
  }, []);

  const handleCollectionClick = (collection: string) => {
    const newSelectedCollections = selectedCollections.includes(collection)
      ? selectedCollections.filter((c) => c !== collection)
      : [...selectedCollections, collection];

    setSelectedCollections(newSelectedCollections);
    onCollectionSelect(newSelectedCollections);
  };

  const handleRefresh = (collection: string) => {
    fetch(`http://localhost:8000/collections/refresh/${collection}`, {
      method: 'GET',
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response data as needed
      });
  };

  const handleDelete = () => {
    fetch(`http://localhost:8000/collections/${collectionToDelete}`, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then((data) => {
        // Remove the deleted collection from the state
        setCollections(collections.filter((c) => c !== collectionToDelete));
        setDeleteDialogOpen(false);
      });
  };

  return (
      <div
          style={{
            // display: 'flex',
            // overflow: 'hidden',
            // flex: '0 1 auto',
            // backgroundColor: 'red',
            // color: 'white',
          }}
      >
      <h2>Context Collections   <AddCollectionButton/> </h2>
        <Dialog
          open={deleteDialogOpen}
          onClose={() => setDeleteDialogOpen(false)}
        >
          <DialogTitle>Delete Collection</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Are you sure you want to delete the collection "{collectionToDelete}"?
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)} color="primary">
              Cancel
            </Button>
            <Button onClick={handleDelete} color="secondary">
              Delete
            </Button>
          </DialogActions>
        </Dialog>
    <Box
      sx={{
        // height: '280px',
        // height: 280,
        overflowY: 'scroll',
        paddingRight: 1,
        borderRight: '1px solid rgba(0, 0, 0, 0.12)',
      }}
    >
      <List>
        {collections.map((collection) => (
          <ListItem
            key={collection}
            button
            onClick={() => handleCollectionClick(collection)}
            selected={selectedCollections.includes(collection)}
          >
            <ListItemText primary={collection} />
            <IconButton
              edge="end"
              color="inherit"
              onClick={(e) => {
                e.stopPropagation();
                handleRefresh(collection);
              }}
            >
              <RefreshIcon />
            </IconButton>
            <IconButton
              edge="end"
              color="inherit"
              onClick={(e) => {
                e.stopPropagation();
                openDeleteDialog(collection);
              }}
            >
              <DeleteIcon />
            </IconButton>
          </ListItem>

        ))}
      </List>
    </Box>
    </div>
  );
};

export default CollectionsList;
