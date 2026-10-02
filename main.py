from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, event, LoggedOutEv
import subprocess
import tempfile
import os
import time
import sys

client = NewClient("luno-bot")

prefix = "."

start_time = None

def is_termux() -> bool:
    return "com.termux" in sys.executable

def enviar_notificacao(title, content):
    if is_termux():
        subprocess.run([
            "termux-notification",
            "--title", title,
            "--content", content,
            "--priority", "high"
        ])
    else:
        from plyer import notification
        notification.notify(
            title=title,
            message=content,
            timeout=10
        )

def webp_convert(midia_bytes: bytes) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_in:
        tmp_in.write(midia_bytes)
        tmp_in_path = tmp_in.name


    tmp_out_path = tmp_in_path.replace(".mp4", "_looped.mp4")

    fps_flag = ["-vsync", "0"] if is_termux() else ["-fps_mode", "vfr"]

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", tmp_in_path,
            "-t", "6",
            "-c", "copy",
            *fps_flag,
            tmp_out_path
        ], check=True, capture_output=True)

        with open(tmp_out_path, "rb") as f:
            return f.read()

    finally:
        os.unlink(tmp_in_path)
        if os.path.exists(tmp_out_path):
            os.unlink(tmp_out_path)

def get_media_message(ev):
    if ev.Message.imageMessage.URL or ev.Message.videoMessage.URL:
        return ev.Message

    quoted = ev.Message.extendedTextMessage.contextInfo.quotedMessage
    if quoted.imageMessage.URL or quoted.videoMessage.URL:
        return quoted

    return None

@client.event(ConnectedEv)
def on_connected(client: NewClient, ev: ConnectedEv):
    global start_time
    start_time = time.time()
    print("🚀 - Bot Conectado com Sucesso!")

@client.event(LoggedOutEv)
def on_logged_out(client: NewClient, ev: LoggedOutEv):
    enviar_notificacao(
        "⚠️ Bot desconectado!",
        "A sessão do WhatsApp expirou. Escaneie o QR code novamente."
    )

@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv):
    texto = (
        ev.Message.conversation
        or ev.Message.extendedTextMessage.text
        or ev.Message.imageMessage.caption
        or ev.Message.videoMessage.caption
    )

    if not texto or not texto.startswith(prefix):
        return

    comando = texto[len(prefix):]

    match comando:
        case "ping":
            latency_ms = round(time.time() * 1000 - ev.Info.Timestamp)

            if start_time:
                uptime = int(time.time() - start_time)
                days, remainder = divmod(uptime, 86400)
                hours, remainder = divmod(remainder, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
            else:
                uptime_str = "N/A"

            client.reply_message(f"🚀 *BOT ONLINE*! \n\n📡 Latência: `{latency_ms}ms`\n⏱️ Uptime: `{uptime_str}`", ev)

        case "figurinha" | "fig" | "f":
            midia_msg = get_media_message(ev)

            if midia_msg is None:
                client.reply_message(f"ERRO! Mande uma foto, video ou gif junto com o comando *{prefix}figurinha*, ou use o comando respondendo uma mensagem com mídia! 📸", ev)
                return

            client.reply_message("Produzindo sua figurinha! Por favor, aguarde!", ev)

            is_video = bool(midia_msg.videoMessage.URL)

            midia_bytes = client.download_any(midia_msg)

            if midia_bytes:
                if is_video:
                    midia_bytes = webp_convert(midia_bytes)
                client.send_sticker(
                    ev.Info.MessageSource.Chat,
                    midia_bytes,
                    quoted=ev,
                    crop=False,
                    enforce_not_broken=True
                )
        case _:
            pass

client.connect()
event.wait()