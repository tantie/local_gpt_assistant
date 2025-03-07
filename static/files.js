async function loadFileStructure() {
    let response = await fetch("/get-structure");
    let data = await response.json();
    console.log("📂 Полученная структура:", data.structure);

    let container = document.getElementById("file_structure");
    container.innerHTML = renderTree(data.structure);
}

function renderTree(data, path = "") {
    let html = "<ul>";
    Object.entries(data).forEach(([key, value]) => {
        let fullPath = path ? `${path}/${key}` : key;

        if (typeof value === "object" && Object.keys(value).length > 0) {
            html += `<li>
                        <span onclick="toggleFolder(this)">📁 ${key}</span>
                        <input type="checkbox" class="folder-checkbox" data-path="${fullPath}" onchange="toggleFolderCheckbox(this)">
                        ${renderTree(value, fullPath)}
                    </li>`;
        } else {
            html += `<li>
                        <input type="checkbox" name="files" value="${fullPath}" onchange="updateSelectedFiles()" disabled>
                        ${key}
                    </li>`;
        }
    });
    return html + "</ul>";
}

function toggleFolderCheckbox(checkbox) {
    let folder = checkbox.closest("li");
    let childCheckboxes = folder.querySelectorAll("input[name='files']");
    childCheckboxes.forEach(child => child.checked = checkbox.checked);
    updateSelectedFiles();
}

async function updateSelectedFiles() {
    let selectedFiles = Array.from(document.querySelectorAll("input[name='files']:checked"))
                             .map(checkbox => checkbox.value);

    let chatElement = document.querySelector(".selected-chat");
    let chatId = chatElement ? chatElement.textContent.trim() : null;

    if (!chatId) return;

    await fetch("/select-files", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ files: selectedFiles, chat_id: chatId })
    });
}

async function loadFilesForChat(chatId) {
    let response = await fetch(`/get-files-for-chat?chat_id=${chatId}`);
    let data = await response.json();

    document.querySelectorAll("input[name='files']").forEach(checkbox => {
        checkbox.checked = data.files.includes(checkbox.value);
        checkbox.disabled = false;
    });
}

function disableFileSelection(state) {
    document.querySelectorAll("input[name='files']").forEach(checkbox => checkbox.disabled = state);
}

window.onload = () => {
    loadFileStructure();
};
