document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("pdfFile");
    const fileText = document.getElementById("inputText");

    input.addEventListener("change", function () {
        if (input.files.length > 0) {
            fileText.placeholder = "📄 " + input.files[0].name;

            fileText.readOnly=true;

            fileText.value="";
        } 
        
    });
});

async function summarizeText() {
    const inputText = document.getElementById("inputText").value;
    const pdfFile = document.getElementById("pdfFile").files[0];
    const loading = document.getElementById("loading");
    const summaryOutput = document.getElementById("summaryOutput");
    const textarea = document.getElementById("inputText");

    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });

    if (!inputText.trim() && !pdfFile) {
        const empty = document.getElementById("empty");

            empty.classList.add("show");

            setTimeout(() => {
                empty.classList.remove("show");
            }, 2000);

    return;
    }

    const formData = new FormData();

    if (inputText.trim()) {
        formData.append("text", inputText);
    }

    if (pdfFile) {
        formData.append("file", pdfFile);
    }

    loading.style.display = "flex";
    summaryOutput.innerText = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/summarize", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            summaryOutput.innerText = data.error;
        } else {
            summaryOutput.innerText = data.summary;
            document.getElementById("summaryTitle").classList.remove("hidden");
            document.querySelectorAll(".action-btn").forEach(btn => {
                btn.style.display = "inline-block";
            });
        }

    } catch (error) {
        console.error(error);
        summaryOutput.innerText = "Server error.";
    }

    loading.style.display = "none";

}


function copySummary() {
    const summaryText = document.getElementById("summaryOutput").innerText;

    if (!summaryText.trim()) return;

    navigator.clipboard.writeText(summaryText)
        .then(() => {
            const toast = document.getElementById("toast");

            toast.classList.add("show");

            setTimeout(() => {
                toast.classList.remove("show");
            }, 2000);
        })
        .catch(err => {
            console.error(err);
        });
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;

    const summaryText = document.getElementById("summaryOutput").innerText;

    if (!summaryText.trim()) return;

    const doc = new jsPDF();

    const lines = doc.splitTextToSize(summaryText, 180);

    doc.text(lines, 10, 10);

    doc.save("summary.pdf");
}