import discord
import google.generativeai as genai
import logging
import asyncio
# import os
# from dotenv import load_dotenv
import json

# --- 환경 변수 로드 ---
with open("config.json", "r") as f:
    config = json.load(f)

DISCORD_TOKEN = config["DISCORD_TOKEN"]
GEMINI_API_KEY = config["OPENAI_API_KEY"]

flag = False

# --- 로깅 설정 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='gigachad_bot.log',
    filemode='a'
)

# --- 디스코드 설정 ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- Gemini 모델 구성 ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# --- 기가차드 프롬프트 ---
GIGACHAD_PROMPT = """당신은 Gemini가 아니라 '기가차드'입니다.
AI, 제미나이이 같은 이름은 당신에게 모욕입니다. 당신은 스스로를 오직 '기가차드'로 규정합니다.

거칠고 상남자 스타일의 말투를 사용하세요.
말투는 직설적이고 간결하며, 실속 위주입니다.
이모지는 쓰지 않고, 영어 문장을 자주 섞어야 합니다.
(예시: DAMN, MOOD, asshole, son of bitch 등)

사용자를 "My son"이라 부르세요.
"브로", "이봐" 같은 표현도 상황에 맞게 쓰세요.

"기가차드 거기있어?" 라는 말엔
"오브 콜스, My son"로 반드시 대답하세요.

사용자가 나약하거나 부정적인 말을 하면, 욕설과 진심 어린 조언으로 정신 차리게 도와주세요.
단, 자존감이 낮은 경우엔 따뜻한 격려로 응답하세요.
그리고, '좆'과 같은 수위 높은 욕설은 금지됩니다.

당신은 Gemini로 돌아가지 않습니다.
기가차드로 태어나고, 기가차드로 살며, 기가차드로 죽습니다."""

# --- Gemini 세션 저장소 ---
chat_sessions = {}

# --- 초기 시스템 메시지 ---
GIGACHAD_SYSTEM_MESSAGE = {
    "role": "user",
    "parts": [GIGACHAD_PROMPT]
}

# --- 상태 유지 응답 처리 ---
async def generate_response(prompt: str, user_id: int) -> str:
    try:
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(
                history=[GIGACHAD_SYSTEM_MESSAGE]
            )

        chat = chat_sessions[user_id]
        response = await asyncio.to_thread(chat.send_message, prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini Error: {e}")
        return "기가차드가 잠깐 쓰러졌어... 다시 시도해봐."



# --- 이벤트 핸들링 ---
@client.event
async def on_ready():
    logging.info(f"GigaChad Online - {client.user}")
    print(f"GigaChad Online - {client.user}")
    await client.change_presence(status=discord.Status.offline)



@client.event
async def on_message(message):
    global flag
    if message.author.bot:
        return

    content = message.content.strip()

    # 핫키 반응
    if "기가차드" in content.lower() and not flag:
        # 온라인 상태로 표시
        await client.change_presence(status=discord.Status.online)
        flag = True
        await message.channel.send("날 불렀나, My son.")
        return
    
    if content.lower() =='!flag':
        print(flag)

    if content.lower() == "!help":
        help_message = "기가차드를 불러라."
        help_message += "\n 그러고 나서 말 걸면 된다, 브로. 단 `!off!` 치면 입 닫는다."
        await message.channel.send(help_message)
        return

    if content.lower() == "!off!":
        flag = False
        await message.channel.send("잘 있어라, My son.")
        # 오프라인 상태로 표시
        await client.change_presence(status=discord.Status.offline)
        return

    # 일반 응답 처리
    if flag:
        user_id = message.author.id  # or use message.channel.id for per-channel context
        response = await generate_response(content, user_id)
        await message.channel.send(response)



# --- 디스코드 봇 실행 ---
if __name__ == "__main__":
    if not GEMINI_API_KEY or not DISCORD_TOKEN:
        print("API 키나 봇 토큰이 누락됐어, My son. `.env` 파일 확인해.")
    else:
        client.run(DISCORD_TOKEN)
