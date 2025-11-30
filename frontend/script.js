let currentTasks = [];

// 1. ANALYZE (POST)
async function analyze() {
    const input = document.getElementById('jsonInput').value;
    const errorBox = document.getElementById('errorBox');
    const list = document.getElementById('resultsList');
    
    errorBox.classList.add('hidden');
    list.innerHTML = '<div style="padding:20px; text-align:center;">Analyzing & Saving...</div>';

    try {
        if(!input.trim()) throw new Error("Please paste JSON data first.");
        const jsonData = JSON.parse(input);
        
        const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jsonData)
        });

        const data = await response.json();
        if (!response.ok || data.error) throw new Error(data.error || "Server Error");

        currentTasks = data;
        render(currentTasks);

    } catch (err) {
        errorBox.textContent = "Error: " + err.message;
        errorBox.classList.remove('hidden');
        list.innerHTML = '';
    }
}

// 2. SUGGEST (GET Top 3)
async function getSuggestions() {
    const list = document.getElementById('resultsList');
    list.innerHTML = '<div style="padding:20px; text-align:center;">Fetching Top 3...</div>';
    
    try {
        const res = await fetch('http://127.0.0.1:8000/api/tasks/suggest/');
        const data = await res.json();
        
        if(data.suggestions && data.suggestions.length > 0) {
            currentTasks = data.suggestions;
            render(currentTasks);
        } else {
            list.innerHTML = '<div style="padding:20px; text-align:center;">No tasks in DB.</div>';
        }
    } catch (e) {
        list.innerHTML = '<div style="color:red; text-align:center">Connection Error</div>';
    }
}

// 3. RENDER (UI Logic)
function render(tasks) {
    const list = document.getElementById('resultsList');
    list.innerHTML = '';
    
    tasks.forEach(t => {
        let pClass = 'priority-low';
        if (t.score > 100) pClass = 'priority-high';
        else if (t.score > 60) pClass = 'priority-medium';

        list.innerHTML += `
            <div class="task-card ${pClass}">
                <div class="card-top">
                    <span>${t.title}</span>
                    <span style="color: #2563eb">${t.score}</span>
                </div>
                <div class="meta">
                    <span>📅 ${t.due_date}</span>
                    <span>⭐ ${t.importance}/10</span>
                    <span>⏳ ${t.estimated_hours}h</span>
                </div>
                <div class="explanation">💡 ${t.explanation}</div>
            </div>
        `;
    });
}

// 4. RESORT (Client Side)
function resort() {
    const strategy = document.getElementById('sortStrategy').value;
    let sorted = [...currentTasks];

    if (strategy === 'deadline') sorted.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    else if (strategy === 'effort') sorted.sort((a, b) => a.estimated_hours - b.estimated_hours);
    else if (strategy === 'impact') sorted.sort((a, b) => b.importance - a.importance);
    else sorted.sort((a, b) => b.score - a.score);
    
    render(sorted);
}