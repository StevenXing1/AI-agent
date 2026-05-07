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
  stats.textContent = `知识库条目: ${data.qa_count} | 已服务对话: ${data.chat_count}`;
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
    appendMessage(`${data.answer} (匹配分数: ${data.score.toFixed(3)})`, "bot");
  } catch (err) {
    appendMessage("服务异常，请稍后重试。", "bot");
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
    adminTip.textContent = "新增问答成功。";
    qInput.value = "";
    aInput.value = "";
    refreshStats();
  } else {
    adminTip.textContent = "新增失败，请检查输入。";
  }
});

uploadBtn.addEventListener("click", async () => {
  const file = csvFile.files[0];
  if (!file) {
    adminTip.textContent = "请先选择 CSV 文件。";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch("/api/admin/upload-csv", { method: "POST", body: formData });
  const data = await res.json();
  adminTip.textContent = `CSV 导入完成，新增 ${data.inserted} 条。`;
  refreshStats();
});

reloadBtn.addEventListener("click", async () => {
  const res = await fetch("/api/admin/reload-model", { method: "POST" });
  if (res.ok) {
    adminTip.textContent = "模型与知识库已重载。";
  } else {
    adminTip.textContent = "重载失败。";
  }
});

appendMessage("你好，我是你的 AI 客服助手，请问有什么可以帮你？", "bot");
refreshStats();
