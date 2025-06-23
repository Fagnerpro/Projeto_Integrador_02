# Smart Saneamento - Projeto Integrador

Este é um projeto de análise e simulação de dados de saneamento desenvolvido para o curso de IA-2 do SENAI/FATESG, utilizando dados da SANEAGO.

## Estrutura do Projeto

- `App.py` - Servidor Flask com APIs para manipulação de dados
- `index.html` - Interface web para visualização e interação com os dados

## Dependências

### Python
- Flask
- Flask-CORS
- pymongo
- pandas
- scikit-learn

### MongoDB
O projeto utiliza MongoDB como banco de dados. É necessário ter o MongoDB instalado e rodando na porta padrão (27017).

## Configuração e Instalação

### 1. Instalar dependências Python
```bash
pip3 install flask flask-cors pymongo pandas scikit-learn
```

### 2. Instalar e configurar MongoDB

#### Ubuntu/Debian:
```bash
# Instalar MongoDB
sudo apt update
sudo apt install -y mongodb

# Iniciar o serviço
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verificar se está rodando
sudo systemctl status mongodb
```

#### Usando Docker (alternativa):
```bash
# Executar MongoDB em container
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 3. Inicializar dados no MongoDB

O projeto inclui dados fixos para o ano de 2019 que são automaticamente carregados quando necessário. Para popular o banco com dados iniciais, você pode:

1. Executar o servidor Flask
2. Usar a interface web para inserir dados
3. Ou usar a API diretamente para inserir dados via POST

## Como Executar

### 1. Iniciar o servidor Flask
```bash
python3 App.py
```

O servidor estará disponível em: `http://localhost:5000`

### 2. Abrir a interface web
Abra o arquivo `index.html` em um navegador web ou sirva-o através de um servidor web local.

## Funcionalidades

### Interface Web (index.html)
- **Dados Históricos**: Visualização de dados históricos com gráficos interativos
- **Inserção de Dados**: Formulário para adicionar novos dados ao sistema
- **Simulação de Investimentos**: Ferramenta para simular cenários futuros de investimento

### API (App.py)
- `GET /api/dados_historicos` - Buscar dados históricos por período
- `POST /api/inserir_dados` - Inserir novos dados
- `POST /api/limpar_dados_inseridos` - Limpar dados inseridos manualmente
- `POST /api/restaurar_dados_originais` - Restaurar dados originais
- `POST /api/deletar_dados` - Deletar dados específicos
- `GET /api/modelo_regressao` - Obter modelo de regressão linear
- `POST /api/simulacao_investimento` - Simular investimentos futuros

## Estrutura dos Dados

### Dados Operacionais
```json
{
  "ano": 2019,
  "periodo": "12M",
  "agua": {
    "populacao_atendida_mil": 5737.64,
    "indice_atendimento_percentual": 0.97,
    "ligacoes_mil": 2209.858,
    "economias_mil": 2404.565,
    "extensao_rede_km": 30554.64,
    "volume_faturado_mil_m3": 272938,
    "volume_produzido_mil_m3": 382166
  },
  "esgoto": {
    "populacao_atendida_mil": 3701.13,
    "indice_atendimento_percentual": 0.63,
    "indice_atendimento_tratado_percentual": 0.93,
    "ligacoes_mil": 1201.067,
    "economias_mil": 1360.312,
    "extensao_rede_km": 13163.15,
    "volume_faturado_mil_m3": 161741,
    "volume_tratado_mil_m3": 150731
  },
  "investimentos": {
    "agua": 91829,
    "esgoto": 76335,
    "total": 168164
  },
  "indice_perda_agua": 28.58
}
```

## Solução de Problemas

### MongoDB não conecta
1. Verifique se o MongoDB está rodando: `sudo systemctl status mongodb`
2. Verifique se a porta 27017 está disponível: `netstat -tlnp | grep 27017`
3. Reinicie o serviço: `sudo systemctl restart mongodb`

### Erro de CORS
O servidor Flask já está configurado com CORS habilitado. Se ainda houver problemas, verifique se está acessando a partir do mesmo domínio ou use um servidor web local.

### Dados não carregam
1. Verifique se o servidor Flask está rodando
2. Verifique se o MongoDB tem dados (use a função "Restaurar Dados Originais")
3. Verifique o console do navegador para erros JavaScript

## Tecnologias Utilizadas

- **Backend**: Python, Flask, MongoDB
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js, Bootstrap
- **Machine Learning**: scikit-learn (Regressão Linear)
- **Visualização**: Chart.js para gráficos interativos

## Autores

Projeto desenvolvido pela Turma IA-2 do SENAI/FATESG como Projeto Integrador, utilizando dados reais da SANEAGO - Saneamento de Goiás S.A.

