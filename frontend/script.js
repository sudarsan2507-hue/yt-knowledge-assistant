// --- SAFE INITIALIZATION BLOCK ---
const API_BASE = 'http://127.0.0.1:8000';

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        lucide.createIcons();
    }
    console.log("System Initialized: Anime Mode Active");
});

async function processVideo() {
    const urlInput = document.getElementById('videoUrl');
    const url = urlInput.value.trim();
    if (!url) {
        alert("Please enter a URL first! (USER_ERROR)");
        return;
    }

    // UI Updates
    setLoading(true);

    try {
        console.log(`Sending request to ${API_BASE}/process_video...`);
        const response = await fetch(`${API_BASE}/process_video`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        renderResults(data);

    } catch (error) {
        console.error("Processing failed:", error);
        alert(`Error: ${error.message}\nMake sure backend is running on port 8000!`);
    } finally {
        setLoading(false);
    }
}

async function sendChat() {
    const input = document.getElementById('chatInput');
    const box = document.getElementById('chatBox');
    const txt = input.value.trim();

    if (!txt) return;

    // Append User Msg
    addMessage(txt, 'user');
    input.value = '';

    // Disable input temporarily
    const btn = document.getElementById('chatBtn');
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: txt })
        });

        const data = await response.json();
        addMessage(data.answer, 'ai');

    } catch (e) {
        addMessage("Connection Error! (Is backend alive?)", 'ai');
    } finally {
        btn.disabled = false;
    }
}

// --- HELPER FUNCTIONS ---

function setLoading(isLoading) {
    const btn = document.getElementById('processBtn');
    const indicator = document.getElementById('loadingState');

    if (isLoading) {
        btn.disabled = true;
        btn.innerText = "WAIT...";
        indicator.style.display = 'block';
        startFactRotation();
    } else {
        btn.disabled = false;
        btn.innerText = "GO!";
        indicator.style.display = 'none';
        stopFactRotation();
    }
}

function renderResults(data) {
    document.getElementById('resultsArea').style.display = 'block';
    document.getElementById('videoTitle').innerText = data.title || "Unknown Title";
    document.getElementById('mainSummary').innerText = data.summary || "No summary provided.";

    const container = document.getElementById('topicsContainer');
    container.innerHTML = '';

    if (data.topics && Array.isArray(data.topics)) {
        data.topics.forEach(t => {
            let subHtml = t.subtopics.map(s => `
                <div class="subtopic">
                    <strong>${s.name}</strong><br>
                    <span style="font-size: 0.9rem; opacity: 0.8;">${s.summary}</span>
                </div>
            `).join('');

            const el = document.createElement('div');
            el.className = 'topic-item';
            el.innerHTML = `
                <div class="topic-header">
                    <i data-lucide="star" width="16"></i> ${t.title}
                </div>
                <div class="subtopic-list">${subHtml}</div>
            `;
            container.appendChild(el);
        });
    }

    // Render Transcript
    const tBox = document.getElementById('transcriptBox');
    if (data.transcript) {
        tBox.innerHTML = data.transcript.map(s =>
            `<div style="margin-bottom: 0.5rem;"><span style="color: var(--anime-yellow);">${s.time}</span> ${s.text}</div>`
        ).join('');
    }

    if (window.lucide) {
        lucide.createIcons();
    } else {
        console.warn("Lucide library not loaded. Icons will not display.");
    }

    // Scroll to results
    document.getElementById('resultsArea').scrollIntoView({ behavior: 'smooth' });
}

function addMessage(text, sender) {
    const box = document.getElementById('chatBox');
    const div = document.createElement('div');
    div.className = `msg ${sender}`;

    // Allow basic bold formatting
    div.innerHTML = sender === 'ai'
        ? `<strong>AI Chan:</strong> ${text.replace(/\n/g, '<br>')}`
        : text;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

let factInterval;
const FACTS = [
    "AI Fact: Whisper uses 1.55 billion parameters! (Wait, I'm using base model...)",
    "Did you know? YouTube uploads 500 hours of video every minute.",
    "Processing vectors... normalizing tensors... eating RAM...",
    "Hold tight! Generating knowledge from chaos.",
    "Almost there! Just connecting the neural dots."
];

function startFactRotation() {
    const txt = document.querySelector('.loading-text');
    let i = 0;
    factInterval = setInterval(() => {
        txt.innerText = FACTS[i % FACTS.length];
        i++;
    }, 3000);
}

function stopFactRotation() {
    clearInterval(factInterval);
    document.querySelector('.loading-text').innerText = "WORKING ON IT... (~´･_･`)~";
}

function toggleTranscript() {
    const box = document.getElementById('transcriptBox');
    box.style.display = box.style.display === 'none' ? 'block' : 'none';
}
