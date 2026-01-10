async function submitResume() {
    const resumeText = document.getElementById("resumeText").value;
    const resumeFile = document.getElementById("resumeFile").files[0];
    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "Analyzing resume...";

    const formData = new FormData();

    if (resumeText) {
        formData.append("resume_text", resumeText);
    } else if (resumeFile) {
        formData.append("resume_file", resumeFile);
    } else {
        resultsDiv.innerHTML = "Please provide resume text or upload a PDF.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze-resume", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            resultsDiv.innerHTML = data.detail || "Error occurred.";
            return;
        }

        displayResults(data.recommended_jobs);
    } catch (error) {
        resultsDiv.innerHTML = "Failed to connect to server.";
    }
}

function displayResults(jobs) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<h3>Recommended Jobs</h3>";

    jobs.forEach(job => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${job.job_title}</strong> - Similarity: ${job.similarity_score}`;
        resultsDiv.appendChild(div);
    });
}
