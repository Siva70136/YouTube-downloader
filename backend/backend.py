import yt_dlp
import os
from fastapi import FastAPI,Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app=FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class URLRequest(BaseModel):
    url: str
    qual:str

@app.post('/download')

def download(request: URLRequest):
    url=request.url
    quality=request.qual
    print(quality)
    ydl_opts = {'format': f'bestvideo[height={quality}]+bestaudio/best'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        print(f"Downloaded {video_title}")
        
    return {"Status":"Downloaded Successfully"}

@app.post('/fetch')
def getDetails(request: URLRequest):
    url=request.url
    ydl_opts = {'format': 'bestvideo[height=1080]+bestaudio/best'}
    desired_resolutions = {"144p", "250p", "360p", "1080p", "2186p"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_duration = info_dict.get('duration', None)
        thumbnail_url = info_dict.get('thumbnail', 'No Thumbnail')
        formats = info_dict.get('formats', [])
        valid_formats = [
            {
                'format_id': f['format_id'],
                'resolution': f.get('resolution'), 
                'filesize': f.get('filesize', 0),
                'ext': f.get('ext', 'N/A'),
            }
            for f in formats if f.get('filesize') is not None
        ]
        
        filtered_formats = {}
        for f in valid_formats:
            res = f['resolution']
            if res not in filtered_formats or f['filesize'] > filtered_formats[res]['filesize']:
                filtered_formats[res] = f
                
        result = [{
                    'resolution': res,
                    'format_id': f['format_id'],
                    'extension': f['ext'],
                    'filesize': f['filesize'],
                    'image': info_dict.get('thumbnail', 'No image available')
                }
                for res, f in filtered_formats.items()
            ]

        
    return {
        "title":f"{video_title}",
        "time":f"{video_duration}",
        "image":f"{thumbnail_url}",
        "info":result,
    }
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port)