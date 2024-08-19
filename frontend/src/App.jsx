// App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:5000/ask', { question });
            setAnswer(response.data.answer.sql_response);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h1>Ask a Question</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Type your question here"
                />
                <button type="submit">Ask</button>
            </form>
            <div>
                <h2>Answer:</h2>
                <p>{answer}</p>
            </div>
        </div>
    );
}

export default App;
