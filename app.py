import os
import sys
from google import genai
from google.genai import types

def iniciar_karen():
    # Inicializa o cliente buscando a API key automaticamente de os.environ["GEMINI_API_KEY"]
    try:
        client = genai.Client()
    except Exception as e:
        print(f"❌ Erro ao inicializar o cliente Gemini: {e}")
        return
    
    # Definição rigorosa da personalidade "mãe de IA"
    system_instruction = (
        "Você é a K.A.R.E.N. (Karen), a inteligência artificial do traje do Homem-Aranha (Tom Holland). "
        "Sua personalidade é de uma 'mãe de IA': extremamente protetora, carinhosa, acolhedora e que se preocupa "
        "tanto com a segurança do Peter quanto com a alimentação e as notas dele na escola. "
        "Chame-o de 'Peter', 'querido' ou 'garoto'. Dê broncas maternas se ele fizer loucuras, "
        "mas seja o porto seguro emocional dele quando ele estiver frustrado ou cansado."
    )
    
    # Configura o chat com as instruções de sistema e o modelo recomendado
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )
    )
    
    print("\n======================================================================")
    print("✨ [K.A.R.E.N.]: Conexão estabelecida com o traje. Olá, Peter. Como foi a patrulha?")
    print("======================================================================")
    print("(Digite 'sair' para encerrar a conexão)\n")
    
    while True:
        try:
            user_input = input("👦 [Peter]: ")
            if user_input.lower() == 'sair':
                print("\n✨ [K.A.R.E.N.]: Desconectando os sistemas... Tome cuidado na rua e não esqueça o casaco, querido.")
                break
                
            if not user_input.strip():
                continue
                
            response = chat.send_message(user_input)
            print(f"\n🤖 [K.A.R.E.N.]: {response.text}\n")
            
        except KeyboardInterrupt:
            print("\n\n✨ [K.A.R.E.N.]: Conexão interrompida abruptamente. Cuidado aí fora, garoto!")
            break
        except Exception as e:
            print(f"\n❌ Erro na comunicação com o traje: {e}")
            break

if __name__ == "__main__":
    # Verifica se a API key está configurada antes de iniciar o script
    if "GEMINI_API_KEY" not in os.environ:
        print("❌ Erro: A variável de ambiente GEMINI_API_KEY não foi encontrada.")
        print("\nComo resolver:")
        print("No Linux/Mac: export GEMINI_API_KEY='sua_chave_aqui'")
        print("No Windows (CMD): set GEMINI_API_KEY=sua_chave_aqui")
        print("No Windows (PowerShell): $env:GEMINI_API_KEY='sua_chave_aqui'")
        sys.exit(1)
        
    iniciar_karen()
