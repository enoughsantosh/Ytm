from fastapi import FastAPI, Request
import yt_dlp

app = FastAPI()

def get_best_audio_url(video_url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',  # Select the best audio format
        'extract_flat': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info['url'] if 'url' in info else None

@app.get("/")
def home():
    return {"message": "Welcome to the YouTube Audio Extractor API!"}

@app.post("/get_audio_link")
async def fetch_audio_link(request: Request):
    data = await request.json()
    video_url = data.get("url")
    if not video_url:
        return {"error": "No video URL provided!"}

    try:
        audio_url = get_best_audio_url(video_url)
        if audio_url:
            return {"audio_url": audio_url}
        else:
            return {"error": "Failed to retrieve audio URL."}
    except Exception as e:
        return {"error": str(e)}
