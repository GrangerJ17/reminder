async function loadAssignments() {
    const res = await fetch("/todo/");
    const data = await res.json();

    const container = document.getElementById("list");
    container.innerHTML = "";

    Object.entries(data).forEach(([title, info]) => {
        const div = document.createElement("div");
        div.className = "assignment";

        div.innerHTML = `
            <div class="title">${title}</div>
            <div class="meta">
                Due: ${info.due_date} · Course: ${info.course_code}
            </div>
        `;

        container.appendChild(div);
    });
}

loadAssignments();

