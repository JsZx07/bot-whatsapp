from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, event, LoggedOutEv
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message, StickerMessage
from neonize.utils.enum import MediaType
import subprocess
import tempfile
import os
import time
import sys
import shutil

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
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=content,
                timeout=10
            )
        except Exception:
            pass

def webp_convert(midia_bytes: bytes) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_in:
        tmp_in.write(midia_bytes)
        tmp_in_path = tmp_in.name

    tmp_out_path = tmp_in_path.replace(".mp4", ".webp")

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-t", "6",
            "-i", tmp_in_path,
            "-vcodec", "libwebp_anim",
            "-vf", "fps=12,scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2",
            "-compression_level", "6",
            "-q:v", "40",
            "-loop", "0",
            "-preset", "default",
            "-an",
            tmp_out_path
        ], check=True, capture_output=True)

        with open(tmp_out_path, "rb") as f:
            return f.read()

    finally:
        if os.path.exists(tmp_in_path):
            os.unlink(tmp_in_path)
        if os.path.exists(tmp_out_path):
            os.unlink(tmp_out_path)

def send_sticker_webp(client, midia_bytes: bytes, ev):
    upload = client.upload(midia_bytes, MediaType.MediaImage)

    msg = Message(
        stickerMessage=StickerMessage(
            URL=getattr(upload, "url", getattr(upload, "URL", "")),
            directPath=upload.DirectPath,
            mediaKey=upload.MediaKey,
            fileSHA256=upload.FileSHA256,
            fileEncSHA256=upload.FileEncSHA256,
            fileLength=len(midia_bytes),
            mimetype="image/webp",
            isAnimated=True
        )
    )

    client.send_message(ev.Info.MessageSource.Chat, msg)

def get_media_message(ev):
    if (ev.Message.imageMessage and ev.Message.imageMessage.URL) or \
       (ev.Message.videoMessage and ev.Message.videoMessage.URL):
        return ev.Message

    ext = getattr(ev.Message, "extendedTextMessage", None)
    if ext and hasattr(ext, "contextInfo") and ext.contextInfo.HasField("quotedMessage"):
        quoted = ext.contextInfo.quotedMessage
        if (quoted.imageMessage and quoted.imageMessage.URL) or \
           (quoted.videoMessage and quoted.videoMessage.URL):
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

    path = "luno-bot"

    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            print("🗑️ Sessão/banco de dados removido com sucesso (arquivo).")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print("🗑️ Pasta de sessão removida com sucesso.")
        else:
            for file in os.listdir("."):
                if file.startswith("luno-bot"):
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
            print("🗑️ Arquivos da sessão limpos.")
    except FileNotFoundError:
        print("Aviso: Sessão já não existia no disco.")
    except PermissionError:
        print("Erro: O arquivo de sessão está bloqueado pelo processo. Feche o bot antes de apagar.")
    except Exception as e:
        print(f"Erro ao tentar remover a sessão: {e}")

    print("🔄 Reiniciando o bot para gerar um novo QR Code...")
    time.sleep(2)

    os.execv(sys.executable, [sys.executable] + sys.argv)

@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv):
    texto = (
        getattr(ev.Message, "conversation", "")
        or getattr(ev.Message.extendedTextMessage, "text", "")
        or getattr(ev.Message.imageMessage, "caption", "")
        or getattr(ev.Message.videoMessage, "caption", "")
    )

    if not texto or not texto.startswith(prefix):
        return

    comando = texto[len(prefix):].strip()

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

            client.reply_message(f"🚀 *BOT ONLINE*! \n\n📡 Latência: `{abs(latency_ms)}ms`\n⏱️ Uptime: `{uptime_str}`", ev)

        case "figurinha" | "fig" | "f":
            midia_msg = get_media_message(ev)

            if midia_msg is None:
                client.reply_message(f"ERRO! Mande uma foto, video ou gif junto com o comando *{prefix}figurinha*, ou use o comando respondendo uma mensagem com mídia! 📸", ev)
                return

            client.reply_message("Produzindo sua figurinha! Por favor, aguarde!", ev)

            is_video = bool(midia_msg.videoMessage and midia_msg.videoMessage.URL)

            try:
                midia_bytes = client.download_any(midia_msg)

                if midia_bytes:
                    if is_video:
                        midia_bytes = webp_convert(midia_bytes)
                        send_sticker_webp(client, midia_bytes, ev)
                    else:
                        client.send_sticker(
                            ev.Info.MessageSource.Chat,
                            midia_bytes,
                            quoted=ev,
                            crop=False,
                            enforce_not_broken=True
                        )
                else:
                    client.reply_message("⚠️ Não foi possível baixar a mídia. Tente novamente!", ev)
            except Exception as e:
                print(f"Erro ao gerar figurinha: {e}")
                client.reply_message("❌ Ocorreu um erro ao processar sua figurinha.", ev)
        case _:
            pass

session_path = "luno-bot"
if not os.path.exists(session_path):
    print("\n" + "="*50)
    print("📱 Nenhuma sessão ativa encontrada!")
    print("👉 Por favor, abra o WhatsApp no celular e ESCANEIE O QR CODE abaixo para ativar o bot.")
    print("="*50 + "\n")

client.connect()
event.wait()