const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileName.textContent = "Selected: " + fileInput.files[0].name;
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-indigo-500');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-indigo-500');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    fileName.textContent = "Dropped: " + e.dataTransfer.files[0].name;
});