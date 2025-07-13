from fasthtml.common import *

app = FastHTML(hdrs=(Script(src="https://cdn.tailwindcss.com"), Script(src="https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js")))

@app.route("/")
def index():
    return Div(
        H1("🌭 Hotdog or Not?", cls="text-5xl font-bold text-center my-6 bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent"),
        Div("Drop image or click", id="u", cls="flex items-center justify-center w-full max-w-xl p-16 mx-auto border-4 border-dashed rounded-2xl cursor-pointer hover:bg-gray-200"),
        Input(type="file", accept="image/*", id="i", cls="hidden"),
        Img(id="m", cls="w-full max-w-xl mx-auto my-6 rounded-2xl hidden"),
        Div(id="r", cls="text-4xl font-bold text-center my-6"),
        Div(id="c", cls="text-lg text-center text-gray-600"),
        Script("""(async()=>{const{pipeline,env}=await import("https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js");env.allowRemoteModels=true;const[u,i,m,r,c]=["u","i","m","r","c"].map(id=>document.getElementById(id));const cl=await pipeline('image-classification','Xenova/vit-base-patch16-224');r.textContent='Ready!';async function h(f){if(!f)return;m.src=URL.createObjectURL(f);m.style.display='block';r.textContent='Analyzing...';const s=Date.now();const p=await cl(m.src);URL.revokeObjectURL(m.src);const isH=p.slice(0,3).some(x=>x.label.toLowerCase().includes('hotdog')||x.label.toLowerCase().includes('hot dog'));r.innerHTML=isH?'🌭 HOTDOG!!! 🌭':'❌ NOT Hotdog ❌';r.className=`text-4xl font-bold text-center my-6 ${isH?'text-green-500 animate-pulse':'text-red-500'}`;const t=p[0];c.textContent=`${t.label} (${(t.score*100).toFixed(1)}%) - ${((Date.now()-s)/1000).toFixed(2)}s`}u.onclick=()=>i.click();i.onchange=e=>h(e.target.files[0]);u.ondragover=e=>e.preventDefault();u.ondrop=e=>{e.preventDefault();h(e.dataTransfer.files[0])}})()""", type="module"),
        cls="container mx-auto p-8 text-center"
    )

serve()
