from pyrfc import Connection
from openai import OpenAI

# Cliente OpenAI (usando o SDK novo)
client = OpenAI(api_key="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")

# Conexão SAP
conn = Connection(
    user='rgodoy',
    passwd='God691410a',
    ashost='10.168.132.5',
    sysnr='08',
    client='200',
    lang='PT',
    saprouter='/H/vpn.exakta.com.br'
)

def consulta_nome_matricula(matricula):
    result = conn.call(
        'RFC_READ_TABLE',
        QUERY_TABLE='PA0002',
        DELIMITER='|',
        ROWCOUNT=1,
        OPTIONS=[{"TEXT": f"PERNR = '{matricula}'"}],
        FIELDS=[{"FIELDNAME": "GBDAT"}]  # Data de nascimento
    )
    for linha in result['DATA']:
        return f"Data de nascimento: {linha['WA']}"
    return "Funcionário não encontrado."

# Chat com IA
while True:
    pergunta = input("Você: ")
    if pergunta.lower() in ["sair", "exit"]:
        break

    if "funcionário" in pergunta and "nascimento" in pergunta:
        matricula = input("Digite a matrícula: ")
        mensagem = consulta_nome_matricula(matricula)
    else:
        resposta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda com informações do SAP ECC."},
                {"role": "user", "content": pergunta}
            ]
        )
        mensagem = resposta.choices[0].message.content

    print("🤖:", mensagem)