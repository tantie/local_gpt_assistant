async function loadChats() {
    let response = await fetch("/get-chats");
    let data = await response.json();
    let chatList = document.getElementById("chat_list");
    chatList.innerHTML = "";

    data.chats.forEach(chat => {
        let li = document.createElement("li");
        li.textContent = chat;
        li.onclick = () => selectChat(chat);
        chatList.appendChild(li);
    });

    disableInputs(true);
}

async function createChat() {
    let chatName = prompt("Введите название нового чата:");
    if (!chatName) return;

    await fetch("/create-chat", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ chat_id: chatName })
    });

    loadChats();
    selectChat(chatName);
}

async function selectChat(chatName) {
    document.querySelectorAll("#chat_list li").forEach(li => li.classList.remove("selected-chat"));
    let selectedChat = Array.from(document.querySelectorAll("#chat_list li"))
        .find(li => li.textContent === chatName);
    if (selectedChat) selectedChat.classList.add("selected-chat");

    document.getElementById("delete_chat_button").disabled = false;
    document.getElementById("delete_chat_button").setAttribute("data-chat", chatName);

    await loadChatHistory(chatName);
    await loadFilesForChat(chatName);

    disableInputs(false);
}

async function deleteChat() {
    let chatName = document.getElementById("delete_chat_button").getAttribute("data-chat");
    if (!chatName) {
        alert("Выберите чат для удаления!");
        return;
    }

    if (!confirm(`Вы уверены, что хотите удалить чат \"${chatName}\"?`)) {
        return;
    }

    await fetch("/delete-chat", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ chat_id: chatName })
    });

    document.getElementById("delete_chat_button").disabled = true;
    document.getElementById("chat_response").innerHTML = "";
    loadChats();

    disableInputs(true);
}

async function loadChatHistory(chatName) {
    let response = await fetch(`/get-chat-history?chat_id=${chatName}`);
    let data = await response.json();
    let chatBox = document.getElementById("chat_response");
    chatBox.innerHTML = data.history.map(msg => `<p><b>${msg.role}:</b> ${msg.content}</p>`).join("");
}

async function loadFilesForChat(chatId) {
    let response = await fetch(`/get-files-for-chat?chat_id=${chatId}`);
    let data = await response.json();

    document.querySelectorAll("input[name='files']").forEach(checkbox => {
        checkbox.checked = data.files.includes(checkbox.value);
        checkbox.disabled = false;
    });
}

function disableInputs(state) {
    document.getElementById("user_message").disabled = state;
    document.querySelectorAll("input[name='files']").forEach(checkbox => checkbox.disabled = state);
    document.querySelector("button[onclick='sendChat()']").disabled = state;
}

window.onload = () => {
    loadChats();
    loadFileStructure();
};
