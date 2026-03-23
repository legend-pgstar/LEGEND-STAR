import os
import asyncio
import traceback
import httpx
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")

HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def post_log(data: dict):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(f"{BACKEND_URL}/log", json=data, headers=HEADERS)
    except Exception as e:
        print("post_log error", e)


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


async def execute_control_loop():
    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(f"{BACKEND_URL}/control", headers=HEADERS)
                actions = res.json()

            for action in actions:
                action_id = action.get("id")
                if action.get("action") == "send_message":
                    channel_id = action.get("channel_id")
                    message_text = action.get("message")
                    try:
                        channel = bot.get_channel(int(channel_id)) or await bot.fetch_channel(int(channel_id))
                        if channel:
                            await channel.send(message_text)
                            await post_log({
                                "type": "system",
                                "user": "control-executor",
                                "content": f"Sent control message to {channel_id}",
                                "command": "send_message",
                                "channel_id": channel_id,
                                "time": now_iso(),
                            })
                            # ack action done
                            await client.post(
                                f"{BACKEND_URL}/control/ack",
                                json={"action_id": action_id, "status": "done"},
                                headers=HEADERS,
                            )
                        else:
                            raise ValueError("Channel not found")

                    except Exception as err:
                        await post_log({
                            "type": "error",
                            "user": "control-executor",
                            "content": f"Control send failed: {err}",
                            "command": "send_message",
                            "channel_id": channel_id,
                            "time": now_iso(),
                        })
                        await client.post(
                            f"{BACKEND_URL}/control/ack",
                            json={"action_id": action_id, "status": "failed"},
                            headers=HEADERS,
                        )

            await asyncio.sleep(5)

        except Exception as e:
            print("control loop error", e)
            await asyncio.sleep(5)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await post_log({
        "type": "system",
        "content": "Bot started",
        "time": now_iso(),
    })


@bot.command(name="send")
async def send(ctx, channel_id: int, *, message: str):
    try:
        channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
        if not channel:
            await ctx.send("Channel not found")
            return

        await channel.send(message)
        await post_log({
            "type": "command",
            "user": str(ctx.author),
            "user_id": ctx.author.id,
            "guild": str(ctx.guild) if ctx.guild else "DM",
            "command": "send_message",
            "content": message,
            "time": now_iso(),
        })
        await ctx.send("Message sent")

    except Exception as e:
        tb = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        await post_log({
            "type": "error",
            "user": str(ctx.author),
            "user_id": ctx.author.id,
            "guild": str(ctx.guild) if ctx.guild else "DM",
            "error": str(e),
            "content": tb,
            "time": now_iso(),
        })
        await ctx.send(f"Error sending message: {e}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    payload = {
        "type": "message",
        "user": str(message.author),
        "user_id": message.author.id,
        "guild": str(message.guild) if message.guild else "DM",
        "content": message.content,
        "time": now_iso(),
    }
    await post_log(payload)
    await bot.process_commands(message)


@bot.event
async def on_command(ctx):
    await post_log({
        "type": "command",
        "user": str(ctx.author),
        "user_id": ctx.author.id,
        "guild": str(ctx.guild) if ctx.guild else "DM",
        "command": ctx.command.name if ctx.command else "unknown",
        "content": ctx.message.content,
        "time": now_iso(),
    })


@bot.event
async def on_command_error(ctx, error):
    tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    await post_log({
        "type": "error",
        "user": str(ctx.author),
        "user_id": ctx.author.id,
        "guild": str(ctx.guild) if ctx.guild else "DM",
        "error": str(error),
        "content": tb,
        "time": now_iso(),
    })


@bot.event
async def on_member_join(member):
    await post_log({
        "type": "system",
        "user": str(member),
        "user_id": member.id,
        "guild": str(member.guild),
        "content": "Member join",
        "time": now_iso(),
    })


if __name__ == "__main__":
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN is required")

    bot.loop.create_task(execute_control_loop())
    bot.run(DISCORD_TOKEN)
