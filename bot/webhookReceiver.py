from extensions.updates import write
from datetime import datetime
from flask import json, request, Flask

app = Flask(__name__)


@app.route("/webhook/github", methods=["POST"])
def github():
    if request.headers["Content-Type"] == 'application/json':
        req = request.json
        added, modified, removed = [], [], []
        data = {"repo": req["repository"]["name"], "count": len(req["commits"]), "commits": []}
        for head in req["commits"]:
            added += head["added"]
            modified += head["modified"]
            removed += head["removed"]
            data["commits"].append({"author": req["sender"]["login"],
                                    "author_avatar": req["sender"]["avatar_url"],
                                    "author_url": req["sender"]["html_url"],
                                    "message": head["message"].rsplit("\n\n", 1),
                                    "time": datetime.strptime(head["timestamp"][:-6], '%Y-%m-%dT%H:%M:%S')})
        total = len(added) + len(modified) + len(removed)
        changes = "\n".join([f"Updated `{total}` files:" if total > 0 else "",
                             (f"**Added** (`{len(added)}`): " + ", ".join(f"`{file}`" for file in added) if added else ""),
                             (f"**Modified** (`{len(modified)}`): " + ", ".join(f"`{file}`" for file in modified) if modified else ""),
                             (f"**Removed** (`{len(removed)}`): " + ", ".join(f"`{file}`" for file in removed) if removed else "")])
        data.update({"changes": changes})
        write(str(data))
        return json.dumps(request.json)


if __name__ == "__main__":
    app.run(debug=True)
