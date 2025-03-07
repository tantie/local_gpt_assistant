async function sendChat() {
    let userMessage = document.getElementById("user_message").value.trim();
    if (!userMessage) {
        alert("Введите сообщение перед отправкой!");
        return;
    }

    let chatElement = document.querySelector(".selected-chat");
    let chatId = chatElement ? chatElement.textContent.trim() : null;

    if (!chatId) {
        alert("Пожалуйста, выберите или создайте чат перед отправкой сообщения.");
        return;
    }

    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ chat_id: chatId, user_message: userMessage })
    });

    let data = await response.json();

    if (response.ok) {
        document.getElementById("chat_response").innerHTML += 
            `<p><b>Вы:</b> ${userMessage}</p><p><b>GPT:</b> ${data.response}</p>`;
    } else {
        alert(`Ошибка: ${data.error}`);
    }
}

function sendPresetPrompt() {
    let presetSelect = document.getElementById("preset_prompt");
    let selectedPrompt = presetSelect.value;
    let promptText = "";

    switch (selectedPrompt) {
        case "describe":
            promptText = "Опиши, что делает этот код.";
            break;
        case "find_bugs":
            promptText = "Найди возможные ошибки в этом коде.";
            break;
        case "optimize":
            promptText = "Как можно оптимизировать этот код?";
            break;
        case "architecture":
            promptText = "Как правильно организовать архитектуру проекта?";
            break;
        case "add_feature":
            promptText = "Как добавить новую функцию в этот код?";
            break;
        default:
            alert("Ошибка: выбран неизвестный запрос.");
            return;
    }

    document.getElementById("user_message").value = promptText;
    sendChat();
}

async function updateGPTData() {
    let response = await fetch("/get-gpt-data");
    let data = await response.json();
    document.getElementById("gpt_data").innerText = data.content;
}

window.onload = () => {
    loadChats();
    loadFileStructure();
    updateGPTData();
};
