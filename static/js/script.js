document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generation-form');
    const outputText = document.getElementById('generated-text');
    const statusElement = document.getElementById('status');
    const tgiUrlElement = document.getElementById('tgi-url');
    const apiUrlElement = document.getElementById('api-url');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const prompt = document.getElementById('prompt').value;
        const temperature = document.getElementById('temperature').value;
        const maxLength = document.getElementById('max-length').value;
        const topK = document.getElementById('top-k').value;

        if (prompt.length === 0 || prompt.length > 500) {
            alert('Prompt must be between 1 and 500 characters.');
            return;
        }

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt, temperature, max_length: maxLength, top_k: topK }),
            });

            const data = await response.json();

            if (response.ok) {
                outputText.textContent = data.generated_text;
            } else {
                outputText.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            outputText.textContent = `Error: ${error.message}`;
        }
    });

    async function updateTGIStatus() {
        try {
            const response = await fetch('/tgi_status');
            const data = await response.json();
            statusElement.textContent = data.status;
            statusElement.style.color = data.status === 'OK' ? 'green' : 'red';
            tgiUrlElement.textContent = data.tgi_url;
            apiUrlElement.textContent = data.api_url;
        } catch (error) {
            statusElement.textContent = 'Error fetching status';
            statusElement.style.color = 'red';
            tgiUrlElement.textContent = 'N/A';
            apiUrlElement.textContent = 'N/A';
        }
    }

    // Update TGI status every 30 seconds
    updateTGIStatus();
    setInterval(updateTGIStatus, 30000);
});
