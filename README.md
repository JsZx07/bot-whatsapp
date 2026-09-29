# 🤖 Bot de Figurinhas para WhatsApp

Bot em Python que transforma fotos, vídeos e GIFs em figurinhas do WhatsApp automaticamente, usando um sistema de comandos com prefixo.

Feito com [Neonize](https://github.com/krypton-byte/neonize), uma biblioteca Python que se conecta diretamente ao protocolo do WhatsApp Web (sem precisar de navegador ou API oficial paga).

## ✨ Funcionalidades

- 🖼️ Cria figurinhas a partir de **fotos**, **vídeos** e **GIFs**
- 💬 Funciona tanto com a mídia **enviada com legenda** (`.figurinha`) quanto **respondendo** uma mensagem que já tem mídia
- ⚙️ Sistema de comandos com prefixo (`.`) usando `match/case`
- 🛡️ Tratamento de erro caso o comando seja usado sem nenhuma mídia junto
- 🔌 Conexão via QR Code, com sessão persistente (não precisa escanear toda vez)
- 🔔 Notificação automática quando a sessão do WhatsApp expirar

## 🛠️ Tecnologias

- Python 3.10+
- [Neonize](https://github.com/krypton-byte/neonize) — binding Python para a lib Go [whatsmeow](https://github.com/tulir/whatsmeow)
- ffmpeg (usado internamente pela Neonize para processar vídeo/gif)
- plyer (notificações no Windows/Linux)
- termux-api (notificações no Android via Termux)

## 🚀 Como rodar

### No Linux/Windows

1. Clone o repositório:
   ```bash
   git clone https://github.com/JsZx07/bot-whatsapp
   cd bot-whatsapp
   ```

2. Instale o ffmpeg e o libmagic no sistema:
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg libmagic1

   # Windows: baixe o ffmpeg em https://ffmpeg.org/download.html e adicione ao PATH
   ```

3. Crie um ambiente virtual e instale as dependências Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # no Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Rode o bot:
   ```bash
   python3 main.py
   ```

5. Escaneie o QR Code que aparece no terminal com o WhatsApp (**Aparelhos conectados**)

6. Pronto! Manda `.figurinha` com uma foto/vídeo/gif (ou respondendo um) no chat conectado

---

### No Android (Termux) — recomendado para rodar 24h de graça

1. Instale o [Termux](https://f-droid.org/packages/com.termux/) e o [Termux:API](https://f-droid.org/packages/com.termux.api/) pelo **F-Droid**

2. Instale as dependências do sistema:
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg git termux-api file
   ```

3. Clone o repositório e instale as dependências Python:
   ```bash
   git clone https://github.com/JsZx07/bot-whatsapp
   cd bot-whatsapp
   pip install -r requirements.txt
   ```

4. Rode o bot:
   ```bash
   python3 main.py
   ```

5. Escaneie o QR Code no terminal com o WhatsApp (**Aparelhos conectados**)

#### Deixar rodando 24h automaticamente (opcional)

1. Instale o tmux:
   ```bash
   pkg install tmux
   ```

2. Instale o [Termux:Boot](https://f-droid.org/packages/com.termux.boot/) pelo F-Droid e abra ele pelo menos uma vez

3. Crie o script de inicialização automática:
   ```bash
   mkdir -p ~/.termux/boot
   nano ~/.termux/boot/start-bot.sh
   ```
   Cole isso dentro:
   ```bash
   #!/data/data/com.termux/files/usr/bin/bash
   termux-wake-lock
   cd ~/bot-whatsapp
   tmux new-session -d -s bot 'python3 main.py'
   ```
   Salve com `Ctrl+X` → `Y` → `Enter`

4. Dê permissão de execução:
   ```bash
   chmod +x ~/.termux/boot/start-bot.sh
   ```

5. Reinicie o celular — o bot vai subir automaticamente!

6. Para ver os logs do bot a qualquer momento:
   ```bash
   tmux attach -t bot
   ```

## 📋 Comandos disponíveis

| Comando | O que faz |
|---|---|
| `.figurinha` / `.fig` / `.f` | Transforma a mídia (anexada ou citada) em sticker |
| `.ping` | Testa se o bot está online |

## 📌 Observações

- O arquivo de sessão gerado pela Neonize (`luno-bot`) fica fora do repositório (`.gitignore`) por segurança — ele contém as credenciais da sessão conectada. Nunca suba esse arquivo pro GitHub.
- Este bot usa conexão não-oficial ao protocolo do WhatsApp. Use por sua conta e risco, preferencialmente com um número secundário.
- Quando a sessão expirar (geralmente quando o celular principal fica muito tempo sem internet), o bot envia uma notificação avisando que é necessário escanear o QR Code novamente.

---

Feito por [JsZx07](https://github.com/JsZx07) como projeto de aprendizado em Python e automação.