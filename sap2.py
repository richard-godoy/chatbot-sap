import streamlit as st
from openai import OpenAI
from pyrfc import Connection

# Configurar cliente OpenAI
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

# Função para consultar SAP
def consulta_nascimento(matricula):
    try:
        result = conn.call(
            'RFC_READ_TABLE',
            QUERY_TABLE='PA0002',
            DELIMITER='|',
            ROWCOUNT=1,
            OPTIONS=[{"TEXT": f"PERNR = '{matricula}'"}],
            FIELDS=[{"FIELDNAME": "GBDAT"}]
        )
        st.write("🔍 Resultado bruto do SAP:", result)  # Debug
        for linha in result['DATA']:
            return f"📅 Data de nascimento: {linha['WA']}"
        return "⚠️ Funcionário não encontrado."
    except Exception as e:
        return f"❌ Erro ao consultar SAP: {e}"

# Configurações iniciais do app
st.set_page_config(page_title="Chatbot SAP", page_icon="🤖")
st.title("🤖 Chatbot SAP ECC")

# Inicializa sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "esperando_matricula" not in st.session_state:
    st.session_state.esperando_matricula = False

# Exibe entrada do usuário
pergunta = st.chat_input("Digite sua pergunta...")

# Processo: etapa 1 - pergunta do usuário
if pergunta and not st.session_state.esperando_matricula:
    st.session_state.historico.append(("Você", pergunta))

    if "nascimento" in pergunta.lower() and "funcionário" in pergunta.lower():
        st.session_state.esperando_matricula = True
        st.session_state.historico.append(("SAP", "Qual é a matrícula do funcionário?"))
    else:
        resposta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda com SAP ECC."},
                {"role": "user", "content": pergunta}
            ]
        )
        conteudo = resposta.choices[0].message.content
        st.session_state.historico.append(("ChatGPT", conteudo))

# Processo: etapa 2 - usuário responde matrícula
if st.session_state.esperando_matricula:
    matricula = st.text_input("Digite a matrícula para continuar:")
    if matricula:
        resposta = consulta_nascimento(matricula)
        st.session_state.historico.append(("SAP", resposta))
        st.session_state.esperando_matricula = False

# Exibe o histórico
for remetente, msg in st.session_state.historico:
    with st.chat_message(remetente):
        st.markdown(msg)

