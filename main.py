from fasthtml.common import *

# FastHTML app with custom headers for Transformers.js
app = FastHTML(
    hdrs=(
        # Transformers.js for browser-based ML
        Script(src="https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js"),
        # Custom styles
        Style("""
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .upload-area { 
                border: 3px dashed #ccc; 
                border-radius: 10px; 
                padding: 50px; 
                text-align: center; 
                transition: all 0.3s ease;
                cursor: pointer;
                margin: 20px 0;
            }
            .upload-area:hover { border-color: #007bff; background-color: #f8f9fa; }
            .upload-area.dragover { border-color: #007bff; background-color: #e3f2fd; }
            .result { 
                margin: 20px 0; 
                padding: 20px; 
                border-radius: 10px; 
                text-align: center; 
                font-size: 24px; 
                font-weight: bold;
                display: none;
            }
            .hotdog { background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; }
            .not-hotdog { background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb; }
            .loading { background-color: #fff3cd; color: #856404; border: 2px solid #ffeaa7; }
            .preview { max-width: 100%; max-height: 300px; border-radius: 10px; margin: 10px 0; }
            .confidence { font-size: 14px; margin-top: 10px; opacity: 0.8; }
            .model-status { 
                position: fixed; 
                top: 10px; 
                right: 10px; 
                padding: 5px 10px; 
                border-radius: 5px; 
                font-size: 12px; 
                background-color: #fff3cd; 
                color: #856404; 
                display: none;
            }
        """)
    )
)

rt = app.route

@rt("/")
def index():
    return Titled(
        "🌭 Hot Dog or Not Hot Dog",
        Div(
            # Model loading status
            Div("Loading AI model...", id="model-status", cls="model-status"),
            
            # Upload area
            Div(
                H3("Drop an image here or click to upload"),
                P("I'll tell you if it's a hot dog or not!"),
                Input(type="file", accept="image/*", id="imageInput", style="display: none;"),
                id="uploadArea",
                cls="upload-area"
            ),
            
            # Preview and result areas
            Div(id="preview"),
            Div(id="result", cls="result"),
            
            # JavaScript for image processing
            Script("""
                let classifier = null;
                let modelLoaded = false;
                
                // Initialize the model
                async function initModel() {
                    try {
                        const modelStatus = document.getElementById('model-status');
                        modelStatus.style.display = 'block';
                        modelStatus.textContent = 'Loading AI model...';
                        
                        // Use a lightweight image classification model
                        const { pipeline } = transformers;
                        classifier = await pipeline('image-classification', 'Xenova/mobilenet_v2_1.4_224');
                        
                        modelLoaded = true;
                        modelStatus.textContent = 'AI model ready!';
                        setTimeout(() => {
                            modelStatus.style.display = 'none';
                        }, 2000);
                    } catch (error) {
                        console.error('Error loading model:', error);
                        document.getElementById('model-status').textContent = 'Error loading model';
                    }
                }
                
                // Initialize model when page loads
                initModel();
                
                // Handle file upload
                const uploadArea = document.getElementById('uploadArea');
                const imageInput = document.getElementById('imageInput');
                const preview = document.getElementById('preview');
                const result = document.getElementById('result');
                
                uploadArea.addEventListener('click', () => imageInput.click());
                
                // Drag and drop handlers
                uploadArea.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    uploadArea.classList.add('dragover');
                });
                
                uploadArea.addEventListener('dragleave', () => {
                    uploadArea.classList.remove('dragover');
                });
                
                uploadArea.addEventListener('drop', (e) => {
                    e.preventDefault();
                    uploadArea.classList.remove('dragover');
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        handleImage(files[0]);
                    }
                });
                
                imageInput.addEventListener('change', (e) => {
                    if (e.target.files.length > 0) {
                        handleImage(e.target.files[0]);
                    }
                });
                
                async function handleImage(file) {
                    if (!modelLoaded) {
                        showResult('Please wait for the AI model to load!', 'loading');
                        return;
                    }
                    
                    // Show preview
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="preview">`;
                    }
                    reader.readAsDataURL(file);
                    
                    // Show loading
                    showResult('Analyzing image...', 'loading');
                    
                    try {
                        // Classify the image
                        const predictions = await classifier(file);
                        
                        // Check if it's a hot dog
                        const isHotdog = checkForHotdog(predictions);
                        
                        if (isHotdog.found) {
                            showResult(
                                `🌭 HOT DOG! 🌭<div class="confidence">Confidence: ${(isHotdog.confidence * 100).toFixed(1)}%</div>`, 
                                'hotdog'
                            );
                        } else {
                            showResult(
                                `❌ NOT HOT DOG<div class="confidence">Top prediction: ${predictions[0].label} (${(predictions[0].score * 100).toFixed(1)}%)</div>`, 
                                'not-hotdog'
                            );
                        }
                    } catch (error) {
                        console.error('Error classifying image:', error);
                        showResult('Error analyzing image', 'not-hotdog');
                    }
                }
                
                function checkForHotdog(predictions) {
                    // Keywords that indicate hot dog
                    const hotdogKeywords = ['hot dog', 'hotdog', 'sausage', 'frankfurter', 'wiener', 'bratwurst'];
                    
                    for (const prediction of predictions) {
                        const label = prediction.label.toLowerCase();
                        const confidence = prediction.score;
                        
                        for (const keyword of hotdogKeywords) {
                            if (label.includes(keyword)) {
                                return { found: true, confidence: confidence };
                            }
                        }
                    }
                    
                    return { found: false, confidence: 0 };
                }
                
                function showResult(message, type) {
                    result.innerHTML = message;
                    result.className = `result ${type}`;
                    result.style.display = 'block';
                }
            """),
            
            cls="container"
        )
    )

# Serve the app
if __name__ == "__main__":
    serve()
