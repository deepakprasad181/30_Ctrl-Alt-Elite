let recognition;
let isRecognizing = false;  // Track whether recognition is active
let lastSpokenQuery = "";  // Store the last recognized query

// Function to navigate to the topic selection page with the PDF Base64 string stored in sessionStorage
function navigateToTopicPage() {
    const fileInput = document.getElementById("fileInput");
    const errorMessage = document.getElementById("error-message");
    
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        
        // Check if the file is a valid PDF
        if (file.type !== "application/pdf") {
            errorMessage.textContent = "Please upload a valid PDF file.";
            errorMessage.style.display = "block";
            return;
        }
        
        // Check the file size (max 10 MB)
        if (file.size > 10 * 1024 * 1024) {
            errorMessage.textContent = "File is too large. Please upload a file smaller than 10MB.";
            errorMessage.style.display = "block";
            return;
        }

        // Read the file as a Base64 string
        const reader = new FileReader();
        reader.onloadend = function() {
            const base64String = reader.result.split(',')[1]; // Get Base64 part from data URL
            
            // Store Base64 string in sessionStorage
            sessionStorage.setItem("pdfFile", base64String);
            
            // Navigate to the topic selection page
            window.location.href = "topic_selection.html";
        };
        
        reader.readAsDataURL(file); // Read the file as Base64
    }
}

// Drag and Drop functions
function allowDrop(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    const fileInput = document.getElementById("fileInput");
    
    fileInput.files = event.dataTransfer.files; // Set the file to the input

    // Trigger the file input change event
    navigateToTopicPage();
}

// Trigger file input when drag-and-drop area is clicked
function triggerFileInput() {
    document.getElementById("fileInput").click();
}

// On window load, retrieve the Base64 string from sessionStorage and display the PDF in the iframe
window.onload = function() {
    const pdfBase64 = sessionStorage.getItem("pdfFile");
    
    if (pdfBase64) {
        const iframe = document.getElementById("pdfFrame");
        const pdfDataUrl = "data:application/pdf;base64," + pdfBase64;
        iframe.src = pdfDataUrl;  // Set the PDF Base64 data as the iframe source
    }

    // Initialize Speech Recognition
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";
        recognition.continuous = true;  // Keep recognizing until stopped
        recognition.interimResults = true;

        const queryInput = document.getElementById("query");

        recognition.onresult = (event) => {
            // Only use final result (not interim)
            if (event.results[event.results.length - 1].isFinal) {
                const currentResult = event.results[event.results.length - 1][0].transcript;
                lastSpokenQuery = currentResult;

                // Append the current spoken query to the previous query
                queryInput.value += " " + lastSpokenQuery;  // Concatenate
            }
        };
    }
};

// Toggle Speech Recognition: Start/Stop
function toggleSpeechRecognition() {
    const micButton = document.querySelector(".mic-button");

    if (isRecognizing) {
        recognition.stop();  // Stop recognition
        micButton.style.backgroundColor = "#d9534f";  // Change button color back
    } else {
        recognition.start();  // Start recognition
        micButton.style.backgroundColor = "#5bc0de";  // Change button color to indicate active state
    }

    // Toggle the recognition state
    isRecognizing = !isRecognizing;
}

// Handle form submission
function submitQuery() {
    const queryInput = document.getElementById("query").value.trim();
    if (queryInput) {
        alert(`Submitting query: ${queryInput}`);
    } else {
        alert("Please enter or speak a query before submitting.");
    }
}

// Ensure the topic field is required when a card is clicked
function validateInput(type) {
    const topicField = document.getElementById("topic");
    if (!topicField.value.trim()) {
        document.getElementById("warning").style.display = "block";
    } else {
        document.getElementById("warning").style.display = "none";
        alert(`Selected option: ${type}`);
    }
}
