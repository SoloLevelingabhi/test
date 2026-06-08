from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    info = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        try:
            opts = {
                "quiet": True,
                "skip_download": True
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                data = ydl.extract_info(url, download=False)

            info = {
                "title": data.get("title"),
                "thumbnail": data.get("thumbnail"),
                "duration": data.get("duration"),
                "uploader": data.get("uploader"),
                "formats": [
                    {
                        "format": f.get("format"),
                        "ext": f.get("ext"),
                        "height": f.get("height")
                    }
                    for f in data.get("formats", [])
                ]
            }

        except Exception as e:
            error = str(e)

    return render_template("index.html", info=info, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
