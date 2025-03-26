from flask import Flask, request, send_file, jsonify
import os
from datetime import datetime
import requests
import tempfile
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)

# Variável global para armazenar o ViewState atual
current_view_state = None

def login(session, cnpj, senha):
    """Realiza login no sistema"""
    print(f"Realizando login com CNPJ: {cnpj}")
    
    # Primeiro acessa a página de login para obter o ViewState atual
    login_page_url = "http://confresa.sigaraguaia.com.br:8080/issweb/paginas/login"
    
    try:
        # Obter a página de login para extrair o ViewState
        print("Acessando página de login para obter ViewState...")
        response = session.get(login_page_url)
        
        if response.status_code != 200:
            print(f"Erro ao acessar página de login: {response.status_code}")
            return False
            
        # Extrair o ViewState da página
        html_content = response.text
        view_state = None
        
        # Buscar o ViewState no HTML
        view_state_match = re.search(r'id="javax\.faces\.ViewState" value="([^"]+)"', html_content)
        if view_state_match:
            view_state = view_state_match.group(1)
            print(f"ViewState obtido: {view_state[:20]}...")
        else:
            print("ViewState não encontrado na página")
            return False
        
        # Agora faz o login com o ViewState obtido
        login_url = "http://confresa.sigaraguaia.com.br:8080/issweb/paginas/login"
        
        headers = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Faces-Request': 'partial/ajax',
            'Origin': 'http://confresa.sigaraguaia.com.br:8080',
            'Referer': 'http://confresa.sigaraguaia.com.br:8080/issweb/paginas/login',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }
        
        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'j_idt110',
            'javax.faces.partial.execute': 'j_idt101',
            'javax.faces.partial.render': 'j_idt101',
            'javax.faces.behavior.event': 'action',
            'javax.faces.partial.event': 'click',
            'j_idt101': 'j_idt101',
            'username': cnpj,
            'password': senha,
            'javax.faces.ViewState': view_state
        }
        
        response = session.post(login_url, headers=headers, data=data)
        print(f"Resposta do login: {response.status_code}")
        
        # Verificar se o login foi bem-sucedido
        if response.status_code == 200:
            # Verificar se há alguma mensagem de erro no conteúdo
            if "Usuário e/ou senha inválidos" in response.text:
                print("Login falhou: Usuário e/ou senha inválidos")
                return False
            else:
                print("Login realizado com sucesso!")
                return True
        else:
            print(f"Falha no login. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro durante o login: {str(e)}")
        return False

def pesquisar_notas(session, data_inicio, data_fim):
    """Pesquisa notas fiscais dentro do período especificado"""
    print(f"Pesquisando notas fiscais no período: {data_inicio} a {data_fim}")
    
    try:
        # Acessar a página de pesquisa para obter o ViewState atual
        pesquisa_url = "http://confresa.sigaraguaia.com.br:8080/issweb/paginas/admin/notafiscal/pesquisarNF"
        
        print("Acessando página de pesquisa para obter ViewState...")
        response = session.get(pesquisa_url)
        
        if response.status_code != 200:
            print(f"Erro ao acessar página de pesquisa: {response.status_code}")
            return False
            
        # Extrair o ViewState da página
        html_content = response.text
        
        # Buscar o ViewState no HTML
        view_state_match = re.search(r'id="javax\.faces\.ViewState" value="([^"]+)"', html_content)
        if view_state_match:
            view_state = view_state_match.group(1)
            print(f"ViewState para pesquisa obtido: {view_state[:20]}...")
        else:
            print("ViewState não encontrado na página de pesquisa")
            return False
    
        # Agora realiza a pesquisa com o ViewState obtido
        url = "http://confresa.sigaraguaia.com.br:8080/issweb/paginas/admin/notafiscal/pesquisarNF"
        
        headers = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Faces-Request': 'partial/ajax',
            'Origin': 'http://confresa.sigaraguaia.com.br:8080',
            'Referer': 'http://confresa.sigaraguaia.com.br:8080/issweb/paginas/admin/notafiscal/pesquisarNF',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }
        
        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'form:cbPesquisar',
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'form frmActions',
            'form:cbPesquisar': 'form:cbPesquisar',
            'form': 'form',
            'form:nrNotaNfs': '',
            'form:nrNotaFimNfs': '',
            'form:smcSituacao_focus': '',
            'form:smcSituacao': 'N',
            'form:j_idt488_focus': '',
            'form:j_idt488_input': '',
            'form:tipoPeriodo_focus': '',
            'form:tipoPeriodo_input': 'E',
            'form:dtInicio_input': data_inicio,
            'form:dtFim_input': data_fim,
            'form:j_idt500': '',
            'form:j_idt502': '',
            'form:dtRpsInicio_input': '',
            'form:dtRpsFim_input': '',
            'form:j_idt509_focus': '',
            'form:j_idt509_input': 'MT',
            'form:municipios_input': '',
            'form:municipios_hinput': '',
            'form:listaAtvAtd_focus': '',
            'form:listaAtvAtd_input': 'null',
            'form:j_idt530_input': '',
            'form:j_idt530_hinput': '',
            'form:j_idt532_input': '',
            'form:j_idt532_hinput': '',
            'form:panelFiltrosGerais_collapsed': 'false',
            'form:tipoPessoa_focus': '',
            'form:tipoPessoa_input': 'J',
            'form:j_idt540': '',
            'form:itNomeTom': '',
            'form:j_idt546_focus': '',
            'form:j_idt546_input': 'MT',
            'form:municipiosTomador_input': '',
            'form:municipiosTomador_hinput': '',
            'form:panelFiltrosIntermediario_collapsed': 'false',
            'form:listagem_selection': '',
            'javax.faces.ViewState': view_state
        }
        
        response = session.post(url, headers=headers, data=data)
        print(f"Resposta da pesquisa: {response.status_code}")
        
        if response.status_code == 200:
            print("Pesquisa realizada com sucesso!")
            
            # Extrair o novo ViewState após a pesquisa (para usar no gerar_zip)
            view_state_match = re.search(r'<update id="javax\.faces\.ViewState"><!\[CDATA\[([^\]]+)\]\]></update>', response.text)
            if view_state_match:
                global current_view_state
                current_view_state = view_state_match.group(1)
                print(f"Novo ViewState após pesquisa: {current_view_state[:20]}...")
            else:
                print("Novo ViewState não encontrado na resposta da pesquisa")
            
            return True
        else:
            print(f"Falha na pesquisa. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro durante a pesquisa: {str(e)}")
        return False

def gerar_zip(session, data_inicio, data_fim):
    """Gera e baixa o arquivo ZIP das notas fiscais"""
    print("Gerando e baixando arquivo ZIP...")
    
    global current_view_state
    
    if not current_view_state:
        print("ViewState não disponível para geração do ZIP")
        return None
    
    url = "http://confresa.sigaraguaia.com.br:8080/issweb/paginas/admin/notafiscal/pesquisarNF"
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://confresa.sigaraguaia.com.br:8080',
        'Referer': 'http://confresa.sigaraguaia.com.br:8080/issweb/paginas/admin/notafiscal/pesquisarNF',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    
    data = {
        'form': 'form',
        'form:nrNotaNfs': '',
        'form:nrNotaFimNfs': '',
        'form:smcSituacao_focus': '',
        'form:smcSituacao': 'N',
        'form:j_idt488_focus': '',
        'form:j_idt488_input': '',
        'form:tipoPeriodo_focus': '',
        'form:tipoPeriodo_input': 'E',
        'form:dtInicio_input': data_inicio,
        'form:dtFim_input': data_fim,
        'form:j_idt500': '',
        'form:j_idt502': '',
        'form:dtRpsInicio_input': '',
        'form:dtRpsFim_input': '',
        'form:j_idt509_focus': '',
        'form:j_idt509_input': 'MT',
        'form:municipios_input': '',
        'form:municipios_hinput': '',
        'form:listaAtvAtd_focus': '',
        'form:listaAtvAtd_input': 'null',
        'form:j_idt530_input': '',
        'form:j_idt530_hinput': '',
        'form:j_idt532_input': '',
        'form:j_idt532_hinput': '',
        'form:panelFiltrosGerais_collapsed': 'false',
        'form:tipoPessoa_focus': '',
        'form:tipoPessoa_input': 'J',
        'form:j_idt540': '',
        'form:itNomeTom': '',
        'form:j_idt546_focus': '',
        'form:j_idt546_input': 'MT',
        'form:municipiosTomador_input': '',
        'form:municipiosTomador_hinput': '',
        'form:panelFiltrosIntermediario_collapsed': 'false',
        'form:listagem_selection': '',
        'form:cbGerarZip': '',
        'javax.faces.ViewState': current_view_state
    }
    
    print(f"Fazendo requisição para gerar ZIP com datas: {data_inicio} a {data_fim}")
    print(f"Usando ViewState: {current_view_state[:20]}...")
    response = session.post(url, headers=headers, data=data, stream=True)
    print(f"Status code da resposta: {response.status_code}")
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        content_disp = response.headers.get('Content-Disposition', '')
        
        print(f"Content-Type: {content_type}")
        print(f"Content-Disposition: {content_disp}")
        
        if 'application/zip' in content_type or '.zip' in content_disp:
            print("Encontrado conteúdo ZIP na resposta, retornando")
            return response.content
        else:
            print("Resposta não contém um arquivo ZIP")
            print(f"Primeiros 200 caracteres da resposta: {response.text[:200]}")
    else:
        print(f"Falha ao gerar ZIP. Status code: {response.status_code}")
    
    return None

@app.route('/download_notas', methods=['POST'])
def download_notas():
    try:
        # Obter dados do request
        data = request.get_json()
        cnpj = data.get('cnpj')
        senha = data.get('senha')
        data_inicio = data.get('data_inicio', '01/03/2025')
        data_fim = data.get('data_fim', '31/03/2025')

        # Validar dados obrigatórios
        if not all([cnpj, senha]):
            return jsonify({'error': 'CNPJ e senha são obrigatórios'}), 400

        # Criar sessão e fazer login
        session = requests.Session()
        
        # Não definimos mais o cookie JSESSIONID de forma fixa
        # Deixamos o requests gerenciar as sessões automaticamente
        
        print(f"Iniciando processo com CNPJ: {cnpj}, período: {data_inicio} a {data_fim}")

        if not login(session, cnpj, senha):
            return jsonify({'error': 'Falha no login. Verifique suas credenciais.'}), 401

        # Pesquisar notas
        if not pesquisar_notas(session, data_inicio, data_fim):
            return jsonify({'error': 'Falha ao pesquisar notas fiscais.'}), 500

        # Gerar e baixar ZIP
        zip_content = gerar_zip(session, data_inicio, data_fim)
        if not zip_content:
            return jsonify({'error': 'Falha ao gerar arquivo ZIP.'}), 500

        # Criar arquivo temporário
        temp_dir = tempfile.gettempdir()
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"notas_fiscais_{now}.zip"
        filepath = os.path.join(temp_dir, secure_filename(filename))

        # Salvar arquivo
        with open(filepath, 'wb') as f:
            f.write(zip_content)

        # Retornar arquivo
        return send_file(
            filepath,
            mimetype='application/zip',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro na API: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 