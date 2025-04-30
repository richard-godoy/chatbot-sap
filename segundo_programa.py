from openai import OpenAI

client = OpenAI(api_key="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")


def agente_simples(pergunta):
    resposta = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "Você é um assistente que responde perguntas sobre SAP HCM."},
        {"role": "user", "content": pergunta}
    ])
    return resposta.choices[0].message.content

print(agente_simples("Como configuro férias no SAP HCM?"))