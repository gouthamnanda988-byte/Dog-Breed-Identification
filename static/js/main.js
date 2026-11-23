/*
   Dog Breed Identification - Main JavaScript
   Handles: mobile nav, drag-and-drop upload, image preview,
   file validation, and prediction request.
*/

document.addEventListener('DOMContentLoaded', function () {

    // =============================================
    //  Mobile Navigation Toggle
    // =============================================
    var navToggle = document.getElementById('navToggle');
    var navLinks  = document.getElementById('navLinks');

    if (navToggle) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('open');
        });

        // Close menu when a link is clicked
        var links = navLinks.querySelectorAll('a');
        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener('click', function () {
                navLinks.classList.remove('open');
            });
        }
    }


    // =============================================
    //  Identify Page — Upload & Preview Logic
    // =============================================

    var dropZone       = document.getElementById('dropZone');
    var fileInput      = document.getElementById('fileInput');
    var chooseBtn      = document.getElementById('chooseBtn');
    var previewArea    = document.getElementById('previewArea');
    var previewImg     = document.getElementById('previewImg');
    var predictBtn     = document.getElementById('predictBtn');
    var resetBtn       = document.getElementById('resetBtn');
    var uploadError    = document.getElementById('uploadError');
    var loadingOverlay = document.getElementById('loadingOverlay');
    var resultArea     = document.getElementById('resultArea');
    var dropPrompt     = document.getElementById('dropPrompt');

    // Info display elements
    var fileNameEl       = document.getElementById('fileName');
    var fileSizeEl       = document.getElementById('fileSize');
    var fileTypeEl       = document.getElementById('fileType');
    var fileDimensionsEl = document.getElementById('fileDimensions');

    // Only run upload logic if we are on the identify page
    if (!dropZone) return;

    // Allowed file types
    var ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];
    var MAX_SIZE_MB   = 10;

    // Currently selected file
    var selectedFile = null;


    // ---- Helper: format file size ----
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }


    // ---- Helper: show error message ----
    function showError(message) {
        uploadError.textContent = message;
        uploadError.classList.add('visible');
    }


    // ---- Helper: hide error message ----
    function hideError() {
        uploadError.textContent = '';
        uploadError.classList.remove('visible');
    }


    // ---- Helper: show result card ----
    function showResult(icon, title, message, cssClass) {
        resultArea.innerHTML =
            '<div class="result-card ' + cssClass + '">' +
                '<div class="result-icon">' + icon + '</div>' +
                '<h3>' + title + '</h3>' +
                '<p>' + message + '</p>' +
            '</div>';
    }


    // ---- Helper: render prediction result with top 3 breeds ----
    function renderPredictionResult(data) {
        var topBreed = data.top_breed;
        var topConf = data.top_confidence;
        var top3 = data.top3 || [];

        var top3Html = '';
        for (var i = 0; i < top3.length; i++) {
            var item = top3[i];
            var rank = i + 1;
            var confVal = Math.min(100, Math.max(0, item.confidence));
            top3Html +=
                '<div class="prediction-item">' +
                    '<div class="prediction-header">' +
                        '<span class="prediction-name"><strong>#' + rank + '</strong> ' + item.breed + '</span>' +
                        '<span class="prediction-percent">' + item.confidence.toFixed(2) + '%</span>' +
                    '</div>' +
                    '<div class="confidence-bar-bg">' +
                        '<div class="confidence-bar-fill" style="width: ' + confVal + '%;"></div>' +
                    '</div>' +
                '</div>';
        }

        // Build report download link (uses prediction_id or query string fallback)
        var downloadUrl = data.prediction_id
            ? '/download_report/' + data.prediction_id
            : '/download_report?filename=' + encodeURIComponent(data.filename || '') +
              '&predicted_breed=' + encodeURIComponent(topBreed) +
              '&confidence=' + encodeURIComponent(topConf) +
              '&top3=' + encodeURIComponent(JSON.stringify(top3)) +
              '&model_version=' + encodeURIComponent(data.model_version || 'MobileNetV2-v1') +
              '&created_at=' + encodeURIComponent(data.timestamp || '');

        resultArea.innerHTML =
            '<div class="result-card result-prediction">' +
                '<div class="result-badge">Primary Match</div>' +
                '<h2 class="result-main-breed">' + topBreed + '</h2>' +
                '<p class="result-main-conf">Confidence Score: <strong>' + Number(topConf).toFixed(2) + '%</strong></p>' +
                '<div class="top3-container">' +
                    '<h4 class="top3-title">Top 3 Predicted Breeds</h4>' +
                    top3Html +
                '</div>' +
                '<div class="prediction-actions">' +
                    '<a href="' + downloadUrl + '" class="btn btn-download-report" id="downloadReportBtn">' +
                        '📄 Download Prediction Report (PDF)' +
                    '</a>' +
                '</div>' +
            '</div>';
    }


    // ---- Validate the selected file ----
    function validateFile(file) {
        hideError();

        // Check file type
        if (ALLOWED_TYPES.indexOf(file.type) === -1) {
            showError('Invalid file type. Please upload a JPG, JPEG, or PNG image.');
            return false;
        }

        // Check file size
        if (file.size > MAX_SIZE_MB * 1024 * 1024) {
            showError('File is too large. Maximum allowed size is ' + MAX_SIZE_MB + ' MB.');
            return false;
        }

        return true;
    }


    // ---- Handle a selected file: validate, preview, show info ----
    function handleFile(file) {
        // Clear previous state
        hideError();
        resultArea.innerHTML = '';

        if (!validateFile(file)) {
            return;
        }

        selectedFile = file;

        // Read and display preview
        var reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;

            // Get image dimensions after it loads
            previewImg.onload = function () {
                fileDimensionsEl.textContent =
                    previewImg.naturalWidth + ' x ' + previewImg.naturalHeight + ' px';
            };
        };
        reader.readAsDataURL(file);

        // Fill in file info
        fileNameEl.textContent = file.name;
        fileSizeEl.textContent = formatFileSize(file.size);
        fileTypeEl.textContent = file.type;
        fileDimensionsEl.textContent = 'Loading...';

        // Show preview, hide drop prompt
        previewArea.classList.add('visible');
        dropZone.style.display = 'none';
    }


    // ---- Reset everything back to initial state ----
    function resetUpload() {
        selectedFile = null;
        fileInput.value = '';

        previewImg.src = '';
        fileNameEl.textContent = '\u2014';
        fileSizeEl.textContent = '\u2014';
        fileTypeEl.textContent = '\u2014';
        fileDimensionsEl.textContent = '\u2014';

        previewArea.classList.remove('visible');
        dropZone.style.display = '';
        resultArea.innerHTML = '';
        hideError();
    }


    // =============================================
    //  Event Listeners
    // =============================================

    // "Choose Image" button opens file dialog
    chooseBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        fileInput.click();
    });

    // Clicking anywhere on the drop zone also opens file dialog
    dropZone.addEventListener('click', function () {
        fileInput.click();
    });

    // File selected via dialog
    fileInput.addEventListener('change', function () {
        if (fileInput.files && fileInput.files[0]) {
            handleFile(fileInput.files[0]);
        }
    });


    // ---- Drag & Drop Events ----
    dropZone.addEventListener('dragenter', function (e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', function (e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', function (e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');

        var files = e.dataTransfer.files;
        if (files && files[0]) {
            handleFile(files[0]);
        }
    });


    // ---- Reset button ----
    resetBtn.addEventListener('click', function () {
        resetUpload();
    });


    // ---- Predict button: send image to server ----
    predictBtn.addEventListener('click', function () {
        if (!selectedFile) {
            showError('Please select an image first.');
            return;
        }

        // Show loading overlay
        loadingOverlay.classList.add('visible');
        resultArea.innerHTML = '';

        // Build FormData and send via fetch
        var formData = new FormData();
        formData.append('file', selectedFile);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // Hide loading
            loadingOverlay.classList.remove('visible');

            if (data.success) {
                renderPredictionResult(data);
            } else {
                var icon = (data.is_dog === false) ? '\uD83D\uDC36' : '\u2139\uFE0F'; // 🐶 or ℹ️
                var cardClass = (data.is_dog === false) ? 'result-warning' : 'result-info';
                showResult(
                    icon,
                    data.title || 'Prediction Failed',
                    data.message || 'An error occurred during prediction.',
                    cardClass
                );
            }
        })
        .catch(function (error) {
            loadingOverlay.classList.remove('visible');
            showResult(
                '\u26A0\uFE0F',  // ⚠️
                'Connection Error',
                'Could not reach the server. Please make sure the Flask app is running.',
                'result-info'
            );
            console.error('Prediction error:', error);
        });
    });


    console.log('Identify page ready.');
});
