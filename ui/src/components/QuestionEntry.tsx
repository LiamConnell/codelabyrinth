// ui/src/components/QuestionEntry.tsx
import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';

const QuestionEntry = ({ onSubmit }: { onSubmit: (question: string) => void }) => {
  const [question, setQuestion] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    onSubmit(question);
    setSubmitted(true);
  };

  const handleClear = () => {
    setQuestion('');
    setSubmitted(false);
  };

  return (
    <div>
        <h2>Question</h2>
      <TextField
        label="Enter your question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        fullWidth
        multiline
        rows={4}
        // rowsMax={10}
        inputProps={{ style: { resize: 'both' } }}
        // style={{color:"white"}}
      />
      <Button
        onClick={handleSubmit}
        variant="contained"
        color="primary"
        disabled={submitted}
      >
        Submit
      </Button>
      {submitted && (
        <Button onClick={handleClear} variant="outlined" color="secondary">
          Clear question
        </Button>
      )}
    </div>
  );
};

export default QuestionEntry;
