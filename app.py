from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_BASE = "https://serverless-tooly-gateway-6n4h522y.ue.gateway.dev/facebook/video"


@app.route("/")
def home():
    return jsonify({
        "owner": "Xeon Vro",
        "status": "running"
    })


@app.route("/fb")
def facebook_video():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "success": False,
            "message": "Missing Facebook URL"
        }), 400

    try:
        response = requests.get(
            API_BASE,
            params={"url": url},
            timeout=30
        )

        data = response.json()

        return jsonify({
            "success": data.get("success", False),
            "title": data.get("title", "Untitled"),
            "videos": {
                "hd": {
                    "size": data.get("videos", {}).get("hd", {}).get("size"),
                    "url": data.get("videos", {}).get("hd", {}).get("url")
                },
                "sd": {
                    "size": data.get("videos", {}).get("sd", {}).get("size"),
                    "url": data.get("videos", {}).get("sd", {}).get("url")
                }
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
