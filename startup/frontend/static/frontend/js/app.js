function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}

function jobCard(job) {
    return `
        <article class="card result-card">
            <div class="card-topline">
                <span class="eyebrow">${escapeHtml(job.employment_type || "OPPORTUNITY")}</span>
                <span class="status ${job.is_open ? "status-open" : "status-muted"}">
                    ${job.is_open ? "Open" : "Closed"}
                </span>
            </div>
            <h3>${escapeHtml(job.title)}</h3>
            <p>${escapeHtml(job.description)}</p>
            <div class="meta-row">
                <span>📍 ${escapeHtml(job.location || "Location not specified")}</span>
            </div>
            <a class="text-link" href="/jobs/${job.id}/">View job →</a>
        </article>
    `;
}

function startupCard(startup) {
    return `
        <article class="card result-card">
            <div class="card-topline">
                <span class="eyebrow">${escapeHtml(startup.industry || "STARTUP")}</span>
                <span class="status ${startup.is_hiring ? "status-open" : "status-muted"}">
                    ${startup.is_hiring ? "Hiring" : "Not hiring"}
                </span>
            </div>
            <h3>${escapeHtml(startup.name)}</h3>
            <p>${escapeHtml(startup.description)}</p>
            <div class="meta-row">
                <span>📍 ${escapeHtml(startup.location || "Location not specified")}</span>
            </div>
            <a class="text-link" href="/startups/${startup.id}/">View startup →</a>
        </article>
    `;
}

function emptyBox(message) {
    return `<div class="empty-state">${escapeHtml(message)}</div>`;
}

function errorBox(message) {
    return `<div class="alert alert-error">${escapeHtml(message)}</div>`;
}

function saveStudentId() {
    const id = document.getElementById("student-id").value;
    if (id) {
        localStorage.setItem("startlyStudentId", id);
        alert("Student ID saved.");
    }
}
