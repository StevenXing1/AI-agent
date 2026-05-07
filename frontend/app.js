const chatBox = document.getElementById("chatBox");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const qaForm = document.getElementById("qaForm");
const qInput = document.getElementById("qInput");
const aInput = document.getElementById("aInput");
const csvFile = document.getElementById("csvFile");
const uploadBtn = document.getElementById("uploadBtn");
const reloadBtn = document.getElementById("reloadBtn");
const adminTip = document.getElementById("adminTip");
const stats = document.getElementById("stats");

function appendMessage(text, role = "bot") {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function refreshStats() {
  const res = await fetch("/api/admin/stats");
  const data = await res.json();
  stats.textContent = `Knowledge base entries: ${data.qa_count} | Conversations served: ${data.chat_count}`;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  messageInput.value = "";

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    appendMessage(`${data.answer} (score: ${data.score.toFixed(3)})`, "bot");
  } catch (err) {
    appendMessage("Service error. Please try again later.", "bot");
  }
  refreshStats();
});

qaForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = qInput.value.trim();
  const answer = aInput.value.trim();
  if (!question || !answer) return;

  const res = await fetch("/api/admin/qa", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, answer, source: "ui-manual" }),
  });

  if (res.ok) {
    adminTip.textContent = "Q&A entry added successfully.";
    qInput.value = "";
    aInput.value = "";
    refreshStats();
  } else {
    adminTip.textContent = "Failed to add. Please check your input.";
  }
});

uploadBtn.addEventListener("click", async () => {
  const file = csvFile.files[0];
  if (!file) {
    adminTip.textContent = "Please select a CSV file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch("/api/admin/upload-csv", { method: "POST", body: formData });
  const data = await res.json();
  adminTip.textContent = `CSV import complete. ${data.inserted} entries added.`;
  refreshStats();
});

reloadBtn.addEventListener("click", async () => {
  const res = await fetch("/api/admin/reload-model", { method: "POST" });
  if (res.ok) {
    adminTip.textContent = "Model and knowledge base reloaded.";
  } else {
    adminTip.textContent = "Reload failed.";
  }
});

appendMessage("Hello! I'm your AI support assistant. How can I help you today?", "bot");
refreshStats();
