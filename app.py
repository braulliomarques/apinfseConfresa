from flask import Flask, request, send_file, jsonify
import os
from datetime import datetime
import requests
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

def login(session, cnpj, senha):
    """Realiza login no sistema"""
    print(f"Realizando login com CNPJ: {cnpj}")
    
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
        'javax.faces.ViewState': '-6556763690275595479:1517015910736234634'
    }
    
    response = session.post(login_url, headers=headers, data=data)
    return response.status_code == 200

def pesquisar_notas(session, data_inicio, data_fim):
    """Pesquisa notas fiscais dentro do período especificado"""
    print(f"Pesquisando notas fiscais no período: {data_inicio} a {data_fim}")
    
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
        'javax.faces.ViewState': '145169562814664515:7486073050633527657'
    }
    
    response = session.post(url, headers=headers, data=data)
    return response.status_code == 200

def gerar_zip(session, data_inicio, data_fim):
    """Gera e baixa o arquivo ZIP das notas fiscais"""
    print("Gerando e baixando arquivo ZIP...")
    
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
        'javax.faces.ViewState': '145169562814664515:7486073050633527657'
    }
    
    response = session.post(url, headers=headers, data=data, stream=True)
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        content_disp = response.headers.get('Content-Disposition', '')
        
        if 'application/zip' in content_type or '.zip' in content_disp:
            return response.content
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
        session.cookies.set('JSESSIONID', 'hj3sBGGHUNes03FngSsi-dPz.undefined', 
                          domain='confresa.sigaraguaia.com.br')

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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 