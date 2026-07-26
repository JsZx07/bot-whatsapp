# 🤖 Bot de Figurinhas para WhatsApp

Bot em Python que transforma fotos, vídeos e GIFs em figurinhas do WhatsApp automaticamente, usando um sistema de comandos com prefixo.

Feito com [Neonize](https://github.com/krypton-byte/neonize), uma biblioteca Python que se conecta diretamente ao protocolo do WhatsApp Web (sem precisar de navegador ou API oficial paga).

## ✨ Funcionalidades

- 🖼️ Cria figurinhas a partir de **fotos**, **vídeos** e **GIFs**
- 💬 Funciona tanto com a mídia **enviada com legenda** (`.figurinha`) quanto **respondendo** uma mensagem que já tem mídia
- ⚙️ Sistema de comandos com prefixo (`.`) usando `match/case`
- 🛡️ Tratamento de erro caso o comando seja usado sem nenhuma mídia junto
- 🔌 Conexão via QR Code, com sessão persistente (não precisa escanear toda vez)

## 🛠️ Tecnologias

- Python 3.10+
- [Neonize](https://github.com/krypton-byte/neonize) — binding Python para a lib Go [whatsmeow](https://github.com/tulir/whatsmeow)
- ffmpeg (usado internamente pela Neonize para processar vídeo/gif)

## 🚀 Como rodar

1. Clone o repositório:
   ```bash
   git clone https://github.com/JsZx07/bot-whatsapp
   cd bot-whatsapp
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install neonize
   ```

3. Rode o bot:
   ```bash
   python3 main.py
   ```

4. Escaneie o QR Code que aparece no terminal com o WhatsApp (**Aparelhos conectados**)

5. Pronto! Manda `.figurinha` com uma foto/vídeo/gif (ou respondendo um) no chat conectado

## 📋 Comandos disponíveis

| Comando       | O que faz                                      |
|---------------|-------------------------------------------------|
| `.figurinha`  | Transforma a mídia (anexada ou citada) em sticker |
| `.ping`       | Testa se o bot está online                      |

## 📌 Observações

- O arquivo de sessão (banco de dados gerado pela Neonize) fica fora do repositório (`.gitignore`) por segurança — ele contém as credenciais da sessão conectada.
- Este bot usa conexão não-oficial ao protocolo do WhatsApp. Use por sua conta e risco, preferencialmente com um número secundário.

---

Feito por [JsZx07](https://github.com/JsZx07) como projeto de aprendizado em Python e automação.
