# 🌭 Hot Dog or Not Hot Dog

A blazing-fast image recognition app built with FastHTML and Transformers.js in under 100 lines of code! 

## ✨ Features

- **Zero API calls**: Runs MobileNet directly in your browser
- **Lightning fast**: Instant predictions after model loads
- **No server processing**: All AI happens client-side
- **Mobile-friendly**: Drag & drop or click to upload
- **Confidence scores**: Shows prediction accuracy

## 🚀 How it Works

1. **Browser-based ML**: Uses Transformers.js to run MobileNet v2 locally
2. **Smart detection**: Searches for hot dog keywords in image classifications
3. **Instant results**: No waiting for server responses
4. **Offline-ready**: Works without internet after initial load

## 📦 Deploy to Vercel

1. **Clone and push** to GitHub
2. **Connect to Vercel** and deploy
3. **Done!** Your app is live

Or use Vercel CLI:
```bash
vercel --prod
```

## 🏃 Run Locally

```bash
# Install dependencies
pip install fasthtml uvicorn

# Run the app
python main.py
```

Visit `http://localhost:5001` and start classifying images!

## 🧠 Technical Details

- **Model**: MobileNet v2 (lightweight, ~14MB)
- **Framework**: FastHTML for the web interface
- **ML**: Transformers.js for browser-based inference
- **Deployment**: Vercel serverless functions

## 🎯 Accuracy

The app detects hot dogs by looking for keywords like:
- "hot dog", "hotdog", "sausage", "frankfurter", "wiener", "bratwurst"

Works best with clear images of food items!

Built to showcase how simple modern AI deployment can be. 🤖
