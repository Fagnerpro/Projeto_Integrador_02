# Smart Saneamento - Projeto Integrador

Este é um projeto de análise e simulação de dados de saneamento desenvolvido para o curso de IA-2 do SENAI/FATESG, utilizando dados da SANEAGO.

## Estrutura do Projeto

* `App.py` - Servidor Flask com APIs para manipulação de dados.
* `Analise_metodologia.py` - Script Python que implementa modelos de regressão logística, árvore de decisão e comparação de modelos para análise de metodologia.
* `dashboard_App_completo.py` - Dashboard interativo baseado em Dash/Bootstrap.
* `index.html` - Interface web para visualização e interação com os dados.
* `imagens/` - Pasta com recursos gráficos utilizados nos relatórios e dashboards.
* `requirements.txt` - Lista de dependências Python necessárias.
* `README.md` - Documentação e instruções de uso.

## Dependências

### Python

* Flask
* Flask-CORS
* pymongo
* pandas
* scikit-learn
* matplotlib

### MongoDB

O projeto utiliza MongoDB como banco de dados. É necessário ter o MongoDB instalado e rodando na porta padrão (27017).

## Configuração e Instalação

### 1. Instalar dependências Python

```bash
pip3 install -r requirements.txt
```

### 2. Instalar e configurar MongoDB

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### Usando Docker (alternativa):

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## Como Executar

### 1. Iniciar o servidor Flask

```bash
python3 App.py
```

O servidor estará disponível em: `http://localhost:5000`

### 2. Executar análise de metodologia

```bash
python3 Analise_metodologia.py
```

Isso gerará gráficos e previsões em `projecao_logistica.png`, `projecao_arvore.png` e `comparacao_modelos.png`.

### 3. Abrir a interface web

Abra o arquivo `index.html` em um navegador ou sirva-o por um servidor web local.

## Endpoints da API

* `GET /api/dados_historicos` - Buscar dados históricos por período.
* `POST /api/inserir_dados` - Inserir novos dados.
* `POST /api/limpar_dados_inseridos` - Limpar dados inseridos manualmente.
* `POST /api/restaurar_dados_originais` - Restaurar dados originais.
* `POST /api/deletar_dados` - Deletar dados específicos.
* `GET /api/modelo_regressao` - Obter modelo de regressão linear.
* `POST /api/simulacao_investimento` - Simular investimentos futuros.

## Estrutura dos Dados

### Dados Operacionais (Exemplo JSON)

```json
{
  "ano": 2019,
  "periodo": "12M",
  "agua": { /* ... */ },
  "esgoto": { /* ... */ },
  "investimentos": { /* ... */ },
  "indice_perda_agua": 28.58
}
```

## Solução de Problemas

* **MongoDB não conecta**: Verifique se o serviço está ativo e a porta 27017 livre.
* **Erro de CORS**: O Flask já habilita CORS; valide domínio de acesso.
* **Dados não carregam**: Confirme que o servidor Flask e o MongoDB estão rodando.

## Tecnologias Utilizadas

* **Backend:** Python, Flask, MongoDB
* **Análise:** scikit-learn, pandas, matplotlib
* **Frontend:** HTML5, CSS3, JavaScript, Chart.js, Bootstrap
* **Dashboard:** Dash e Dash Bootstrap Components

## Autores

Projeto desenvolvido pela Turma IA-2 do SENAI/FATESG utilizando dados da SANEAGO - Saneamento de Goiás S.A.

