#!/usr/bin/env python3
import requests
import os
from datetime import datetime
import argparse

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
    
    if response.status_code == 200:
        print("Login realizado com sucesso!")
        return True
    else:
        print(f"Falha no login. Status code: {response.status_code}")
        return False

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
    
    if response.status_code == 200:
        print("Pesquisa realizada com sucesso!")
        return True
    else:
        print(f"Falha na pesquisa. Status code: {response.status_code}")
        return False

def gerar_zip(session, data_inicio, data_fim, output_dir):
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
            # Cria o diretório de saída se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            # Define o nome do arquivo ZIP
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"notas_fiscais_{now}.zip"
            filepath = os.path.join(output_dir, filename)
            
            # Salva o arquivo
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"Arquivo ZIP baixado com sucesso: {filepath}")
            return True
        else:
            print("A resposta não contém um arquivo ZIP. Verifique se existem notas fiscais no período.")
            return False
    else:
        print(f"Falha ao gerar/baixar o ZIP. Status code: {response.status_code}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Automatiza o download de notas fiscais do SIGAR Aguaia')
    parser.add_argument('--cnpj', required=True, help='CNPJ para login')
    parser.add_argument('--senha', required=True, help='Senha para login')
    parser.add_argument('--data-inicio', default='01/03/2025', help='Data de início (formato: DD/MM/AAAA)')
    parser.add_argument('--data-fim', default='31/03/2025', help='Data de fim (formato: DD/MM/AAAA)')
    parser.add_argument('--output-dir', default='./downloads', help='Diretório para salvar o arquivo ZIP')
    
    args = parser.parse_args()
    
    # Cria uma sessão para manter os cookies
    session = requests.Session()
    
    # Adiciona o cookie JSESSIONID inicial (pode ser necessário ou não)
    session.cookies.set('JSESSIONID', 'hj3sBGGHUNes03FngSsi-dPz.undefined', domain='confresa.sigaraguaia.com.br')
    
    # Executa o processo
    if login(session, args.cnpj, args.senha):
        if pesquisar_notas(session, args.data_inicio, args.data_fim):
            gerar_zip(session, args.data_inicio, args.data_fim, args.output_dir)

if __name__ == "__main__":
    main() 