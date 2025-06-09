const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Path to the JSON file
const JSON_FILE = 'quiz_data.json';

// Load existing data from JSON file if it exists
function loadQuizData() {
    if (fs.existsSync(JSON_FILE)) {
        try {
            const data = fs.readFileSync(JSON_FILE, 'utf8');
            return JSON.parse(data);
        } catch (err) {
            return []; // Return empty array if file is empty or corrupted
        }
    }
    return [];
}

// Save quiz data to JSON file
function saveQuizData(data) {
    fs.writeFileSync(JSON_FILE, JSON.stringify(data, null, 4), 'utf8');
}

// Initialize quiz_data by loading from file
let quizData = loadQuizData();

app.get('/api/quiz', (req, res) => {
    res.json(quizData);
});

app.post('/api/quiz', (req, res) => {
    const data = req.body;
    if (!data || !data.question || !data.options || !data.answer) {
        return res.status(400).json({ error: "Invalid data format" });
    }
    quizData.push(data);
    saveQuizData(quizData); // Save to JSON file
    res.status(201).json({ message: "✅ प्रश्न जोड़ा गया!" });
});

app.delete('/api/quiz/:index', (req, res) => {
    const index = parseInt(req.params.index);
    if (index >= 0 && index < quizData.length) {
        const deleted = quizData.splice(index, 1)[0];
        saveQuizData(quizData); // Update JSON file after deletion
        return res.json({ message: `❌ '${deleted.question}' हटाया गया!` });
    }
    res.status(404).json({ error: "Invalid index" });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
