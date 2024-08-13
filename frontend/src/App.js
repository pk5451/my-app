import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [file, setFile] = useState(null);
    const [summary, setSummary] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", file);

        try {
            const uploadResponse = await axios.post('http://localhost:8000/upload', formData);
            console.log(uploadResponse.data);

            const summaryResponse = await axios.post('http://localhost:8000/summarize', formData);
            setSummary(summaryResponse.data.summary);
        } catch (error) {
            console.error("There was an error!", error);
        }
    };

    return (
        <div>
            <h1>Document Summarizer</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload and Summarize</button>
            </form>
            <div>
                <h2>Summary:</h2>
                <p>{summary}</p>
            </div>
        </div>
    );
}

export default App;
