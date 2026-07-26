from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, event

client = NewClient("luno-bot")

prefix = "."

@client.event(ConnectedEv)
def on_connected(client: NewClient, ev: ConnectedEv):
    print("🚀 - Bot Conectado com Sucesso!")

def get_media_message(ev):
    if ev.Message.imageMessage.URL or ev.Message.videoMessage.URL:
        return ev.Message

    quoted = ev.Message.extendedTextMessage.contextInfo.quotedMessage
    if quoted.imageMessage.URL or quoted.videoMessage.URL:
        return quoted

    return None

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
            client.reply_message("Pong! 🏓", ev)
    
        case "figurinha" | "fig":
            midia_msg = get_media_message(ev)

            if midia_msg is None:
                client.reply_message(f"ERRO! Mande uma foto, video ou gif junto com o comando *{prefix}figurinha*, ou use o comando respondendo uma mensagem com mídia! 📸", ev)
                return

            midia_bytes = client.download_any(midia_msg)
            if midia_bytes:
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