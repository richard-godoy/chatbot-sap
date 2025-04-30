from openai import OpenAI

client = OpenAI(api_key="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")

# Coloque sua chave aqui

print("🤖 Chatbot IA - Digite 'sair' para encerrar.")

# Histórico da conversa
conversa = [
    {"role": "system", "content": "Você é um assistente simpático e prestativo."}
]

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Chat encerrado. Até logo! 👋")
        break

    conversa.append({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(model="gpt-4",  # você pode trocar por "gpt-3.5-turbo" se preferir
    messages=conversa)

    mensagem = resposta.choices[0].message.content
    print(f"\n🤖 Chatbot: {mensagem}")

    conversa.append({"role": "assistant", "content": mensagem})
