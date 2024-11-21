document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a file!');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    // Prediction request
    const response = await fetch('/predict/', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    const resultDiv = document.getElementById('result');
    const imageDiv = document.getElementById('image');

    if (result.error) {
        resultDiv.innerHTML = `<h3>Error: ${result.error}</h3>`;
        imageDiv.innerHTML = '';
    } else {
        resultDiv.innerHTML = `<h3>Prediction: ${result.prediction}</h3>`;
        imageDiv.innerHTML = `<img src="${URL.createObjectURL(file)}" alt="Uploaded Image">`;
    }
});