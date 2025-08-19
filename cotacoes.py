#!/usr/bin/env python3
"""
Script para consulta de cotações de moedas em relação ao BRL.
Consulta USD, EUR e GBP via API e salva os dados em arquivo CSV.

Autor: Engenheiro Python Sênior - Claude Sonnet 4
Data: 2025-08-19
"""

import csv
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests


# Configuração de logging
def setup_logging() -> None:
    """Configura o sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cotacoes.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


class CotacaoAPI:
    """Classe para consulta de cotações via API."""
    
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        self.moedas_desejadas = ["USD", "EUR", "GBP"]
        self.timeout = 10
        
    def buscar_cotacoes(self, moeda_base: str = "BRL") -> Optional[Dict]:
        """
        Busca cotações da API.
        
        Args:
            moeda_base: Moeda base para conversão (padrão: BRL)
            
        Returns:
            Dict com dados da API ou None em caso de erro
        """
        url = f"{self.base_url}/{moeda_base}"
        
        try:
            logging.info(f"Consultando API: {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logging.info("Dados recebidos com sucesso da API")
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao consultar API: {e}")
            return None
        except ValueError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
            return None
    
    def extrair_cotacoes_relevantes(self, dados_api: Dict) -> List[Dict]:
        """
        Extrai apenas as cotações das moedas desejadas.
        
        Args:
            dados_api: Dados retornados pela API
            
        Returns:
            Lista de dicionários com cotações formatadas
        """
        cotacoes = []
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if "rates" not in dados_api:
            logging.error("Campo 'rates' não encontrado na resposta da API")
            return cotacoes
        
        rates = dados_api["rates"]
        
        for moeda in self.moedas_desejadas:
            if moeda in rates:
                # Como a API retorna taxas em relação ao BRL,
                # precisamos inverter para obter BRL por unidade da moeda estrangeira
                valor_brl = 1 / rates[moeda] if rates[moeda] != 0 else 0
                
                cotacao = {
                    "data": data_atual,
                    "moeda": moeda,
                    "valor": round(valor_brl, 4)
                }
                cotacoes.append(cotacao)
                logging.info(f"Cotação {moeda}: {valor_brl:.4f} BRL")
            else:
                logging.warning(f"Moeda {moeda} não encontrada na resposta da API")
        
        return cotacoes


class GerenciadorCSV:
    """Classe para gerenciar operações com arquivo CSV."""
    
    def __init__(self, arquivo: str = "cotacoes.csv"):
        self.arquivo = Path(arquivo)
        self.colunas = ["data", "moeda", "valor"]
    
    def arquivo_existe(self) -> bool:
        """Verifica se o arquivo CSV já existe."""
        return self.arquivo.exists()
    
    def criar_cabecalho(self) -> None:
        """Cria arquivo CSV com cabeçalho se não existir."""
        if not self.arquivo_existe():
            try:
                with open(self.arquivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.colunas)
                    writer.writeheader()
                logging.info(f"Arquivo {self.arquivo} criado com cabeçalho")
            except IOError as e:
                logging.error(f"Erro ao criar arquivo CSV: {e}")
                raise
    
    def salvar_cotacoes(self, cotacoes: List[Dict]) -> bool:
        """
        Salva cotações no arquivo CSV.
        
        Args:
            cotacoes: Lista de cotações para salvar
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if not cotacoes:
            logging.warning("Nenhuma cotação para salvar")
            return False
        
        try:
            # Garante que o arquivo existe com cabeçalho
            self.criar_cabecalho()
            
            # Adiciona as novas cotações
            with open(self.arquivo, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.colunas)
                writer.writerows(cotacoes)
            
            logging.info(f"{len(cotacoes)} cotações salvas em {self.arquivo}")
            return True
            
        except IOError as e:
            logging.error(f"Erro ao salvar no CSV: {e}")
            return False


def main():
    """Função principal do script."""
    setup_logging()
    
    logging.info("=== Iniciando consulta de cotações ===")
    
    try:
        # Inicializa os componentes
        api = CotacaoAPI()
        csv_manager = GerenciadorCSV()
        
        # Busca dados da API
        dados_api = api.buscar_cotacoes()
        if not dados_api:
            logging.error("Falha ao obter dados da API. Encerrando execução.")
            sys.exit(1)
        
        # Extrai cotações relevantes
        cotacoes = api.extrair_cotacoes_relevantes(dados_api)
        if not cotacoes:
            logging.error("Nenhuma cotação válida encontrada. Encerrando execução.")
            sys.exit(1)
        
        # Salva no CSV
        sucesso = csv_manager.salvar_cotacoes(cotacoes)
        if not sucesso:
            logging.error("Falha ao salvar cotações. Encerrando execução.")
            sys.exit(1)
        
        logging.info("=== Consulta de cotações concluída com sucesso ===")
        
    except KeyboardInterrupt:
        logging.info("Execução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()