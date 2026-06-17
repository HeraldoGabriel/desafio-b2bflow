import os
import requests
from supabase import create_client
from dotenv import load_dotenv

# Carregar arquivo .env
load_dotenv()

def main():
    
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")) 
    #verificar bd
    try:
    
        response = supabase.table("contatos").select("*").limit(3).execute()
        contatos = response.data
        #pegar dados
        if not contatos:
            print("Nenhum contato encontrado na tabela.")
            return

        for contato in contatos:
            nome = contato.get('nome')
            telefone = contato.get('telefone')
            
            # mensagem pedida (ola *** tudo bm com vc?)
            mensagem = f"Olá, {nome} tudo bem com você?"
            
            payload = {
                "phone": telefone,
                "message": mensagem
            }
            
            # enviar payload para z-api
            response_zapi = requests.post(os.getenv("ZAPI_URL"), json=payload)
            
            if response_zapi.status_code == 200:
                print(f"Sucesso: Mensagem enviada para {nome} ({telefone})")
            else:
                print(f"Erro ao enviar para {nome}: {response_zapi.text}")
                
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()