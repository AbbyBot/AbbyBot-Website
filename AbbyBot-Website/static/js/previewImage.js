const ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif'];

function previewImage(event) {
    const input = event.target;
    const file = input.files[0];
    
    if (!file) {
        return;
    }

    // Check extension
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
        alert('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.');
        input.value = ''; // Clear input if file is invalid
        document.getElementById('image_preview').style.display = 'none';
        return;
    }
    
    // Image preview
    const reader = new FileReader();
    reader.onload = function() {
        const output = document.getElementById('image_preview');
        output.src = reader.result;
        output.style.display = 'block'; // Make image visible
    };
    reader.readAsDataURL(file);
}
