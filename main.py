from fasthtml.common import *

app = FastHTML(hdrs=(
    Script(src="https://cdn.tailwindcss.com"),
    Script(src="https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js")
))

@app.route("/")
def index():
    return (
        Div(
            H1("🌭 Hotdog or Not?", cls="text-5xl font-extrabold text-center my-6 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-pink-500"),
            Div("Drop an image below or click to upload", id="upload",
                cls="flex items-center justify-center w-full max-w-xl p-16 mx-auto border-4 border-dashed rounded-2xl cursor-pointer hover:bg-gray-200 transition-all duration-300 ease-in-out transform hover:scale-105 shadow-md"),
            Input(type="file", accept="image/*", id="inp", cls="hidden"),
            Img(id="img", cls="w-full max-w-xl mx-auto my-6 rounded-2xl hidden shadow-lg"),
            Div(id="res", cls="text-4xl font-bold text-center my-6"),
            Div(id="confidence", cls="text-lg text-center text-gray-600 font-medium"),
            Script(
"""const { pipeline, env } = await import("https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js");
env.allowRemoteModels = true;
const [upload, inp, img, res, confidence] = ['upload', 'inp', 'img', 'res', 'confidence'].map(id => document.getElementById(id));
const classifier = await pipeline('image-classification', 'Xenova/vit-base-patch16-224');
res.textContent = 'Ready!';

async function handleFile(file) {
    if (!file) return;
    img.src = URL.createObjectURL(file);
    img.style.display = 'block';
    res.textContent = 'Analyzing...';
    res.className = 'text-4xl font-bold text-center my-6 text-gray-500';
    confidence.textContent = '';
    const preds = await classifier(img.src);
    URL.revokeObjectURL(img.src);
    const isHotdog = preds.slice(0, 3).some(p => p.label.toLowerCase().includes('hotdog') || p.label.toLowerCase().includes('hot dog'));
    res.innerHTML = isHotdog ? '🌭 HOTDOG!!! 🌭' : '❌ NOT Hotdog ❌';
    res.className = `text-4xl font-bold text-center my-6 ${isHotdog ? 'text-green-500 animate-pulse' : 'text-red-500'}`;
    const topPred = preds[0];
    confidence.textContent = `Top prediction: ${topPred.label} (${(topPred.score * 100).toFixed(1)}%)`;
}

upload.onclick = () => inp.click();
inp.onchange = e => handleFile(e.target.files[0]);
upload.ondragover = e => e.preventDefault();
upload.ondrop = e => { e.preventDefault(); handleFile(e.dataTransfer.files[0]); };
""", type="module"),
            cls="container mx-auto p-8 text-center"
        )
    )
serve()
