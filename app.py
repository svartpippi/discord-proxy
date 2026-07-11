from flask import Flask, request
import requests
import os
import datetime

app = Flask(__name__)

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SEVERITY_COLORS = {
    "critical": 0xFF0000,
    "warning": 0xFFA500,
    "info": 0x00BFFF,
    "none": 0x808080
}

def build_embed(alert):
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    status = alert.get("status", "firing")
    severity = labels.get("severity", "none")

    color = SEVERITY_COLORS.get(severity, 0x808080)

    title = f"{labels.get('alertname', 'Alert')} ({severity})"
    description = annotations.get("description", annotations.get("summary", ""))

    fields = []

    for k, v in labels.items():
        fields.append({"name": k, "value": v, "inline": True})

    for k, v in annotations.items():
        fields.append({"name": k, "value": v, "inline": False})

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": fields,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    if status == "resolved":
        embed["footer"] = {"text": "Resolved"}

    return embed

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    embeds = [build_embed(alert) for alert in data.get("alerts", [])]

    payload = {"embeds": embeds}

    requests.post(WEBHOOK, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9094)
