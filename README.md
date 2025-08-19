Um script Python profissional e robusto criado com claude para consultar cotações de moedas. Aqui estão as principais características do código:
Funcionalidades Principais:

Consulta API: Usa a ExchangeRate-API (gratuita, sem necessidade de chave)
Moedas: Consulta USD, EUR e GBP em relação ao BRL
Formato CSV: Salva com colunas data, moeda, valor
Logging completo: Arquivo cotacoes.log + console
Tratamento de erros: Para requisições, JSON, arquivo e exceções gerais

Estrutura do Código:

Classe CotacaoAPI: Gerencia consultas à API com timeout e tratamento de erros
Classe GerenciadorCSV: Manipula arquivo CSV com cabeçalhos automáticos
Logging configurado: INFO level com timestamps e múltiplos handlers
Arquitetura modular: Separação clara de responsabilidades

Como usar:
bash# Instalar dependência
pip install requests

# Executar o script
python cotacoes.py
Arquivos gerados:

cotacoes.csv: Dados das cotações
cotacoes.log: Logs de execução

Exemplo de saída CSV:
csvdata,moeda,valor
2025-08-19 14:30:15,USD,5.4521
2025-08-19 14:30:15,EUR,5.9876
2025-08-19 14:30:15,GBP,6.9543
O script é robusto, com tratamento completo de erros, logging detalhado e pode ser executado repetidamente para acumular dados históricos no mesmo arquivo CSV.
