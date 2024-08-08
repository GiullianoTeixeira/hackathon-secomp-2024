document.getElementById('imagem1').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewImage = document.getElementById('previewImage');
    
    if (file) {
        // Check if the file is an image and has an allowed extension
        const allowedExtensions = ['image/png', 'image/jpeg'];
        if (allowedExtensions.includes(file.type)) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewImage.alt = file.name;
            };
            reader.readAsDataURL(file);
        } else {
            alert('Please select a valid image file (PNG, JPG, or JPEG).');
            previewImage.src = '';
            previewImage.alt = 'Nenhum arquivo selecionado';
        }
    } else {
        previewImage.src = '';
        previewImage.alt = 'Nenhum arquivo selecionado';
    }
});