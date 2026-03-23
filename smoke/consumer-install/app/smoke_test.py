import json
import os
import urllib.request


BASE_URL = os.environ.get("SMOKE_BASE_URL", "http://localhost:8000").rstrip("/")


def request(path, method="GET", payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        body = response.read().decode("utf-8")
        return response.status, body, dict(response.headers)


status, body, _ = request("/unicom/webchat/demo/")
assert status == 200, f"Unexpected demo status: {status}"
assert "unicom-chat-with-sidebar" in body, "WebChat demo markup missing"

status, body, _ = request("/unicom/webchat/send/", method="POST", payload={"text": "hello from consumer install smoke"})
assert status == 200, f"Unexpected send status: {status}"
send_data = json.loads(body)
assert send_data["success"] is True, body
chat_id = send_data["chat_id"]
message_id = send_data["message"]["id"]

status, body, _ = request(f"/unicom/webchat/messages/?chat_id={chat_id}")
assert status == 200, f"Unexpected messages status: {status}"
messages_data = json.loads(body)
assert messages_data["success"] is True, body
assert any(message["id"] == message_id for message in messages_data["messages"]), body

status, body, _ = request("/unicom/webchat/chats/")
assert status == 200, f"Unexpected chats status: {status}"
chats_data = json.loads(body)
assert chats_data["success"] is True, body
assert any(chat["id"] == chat_id for chat in chats_data["chats"]), body

print("consumer install smoke test passed")
