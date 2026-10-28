import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google import genai

# 환경 변수에서 키 값을 안전하게 불러옵니다
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
GEMINI_API_KEY  = os.environ.get("GEMINI_API_KEY")

app = App(token=SLACK_BOT_TOKEN)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

@app.event("app_mention")
def handle_mention(event, say):
    user_text = event.get("text", "")
    channel = event.get("channel")
    thread_ts = event.get("thread_ts", event.get("ts"))

    prompt = " ".join([word for word in user_text.split() if not word.startswith("<@")])

    if not prompt.strip():
        say(text="궁금한 내용을 적어주세요!", thread_ts=thread_ts)
        return

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        say(text=response.text, thread_ts=thread_ts)
    except Exception as e:
        say(text=f"오류가 발생했습니다: {e}", thread_ts=thread_ts)

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
