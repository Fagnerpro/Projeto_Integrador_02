from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime

def parse_timestamp(ts):
    """Função para converter timestamp em ano"""
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f").year
    except ValueError:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S").year

# Inicialização da aplicação
app = Flask(__name__)
CORS(app)

# Conexão com o MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["saneamento"]
    collection_operacional = db["dados_operacionais"]
    collection_leituras_iot = db["leituras_iot"]
    # Teste de conexão
    client.admin.command('ping')
    print("Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
    print("Certifique-se de que o MongoDB está rodando na porta 27017")



# Dados originais para restauração offline de 2020 a 2024
DADOS_ORIGINAIS_COMPLETOS = {   '2020': {   '12M': {   'agua': {   'economias_mil': 2424.0,
                                       'extensao_rede_km': 30599.0,
                                       'indice_atendimento_percentual': 0.972,
                                       'ligacoes_mil': 2222.0,
                                       'populacao_atendida_mil': 5761.0,
                                       'volume_faturado_mil_m3': 65282.0,
                                       'volume_produzido_mil_m3': 93882.0},
                           'ano': 2020,
                           'esgoto': {   'economias_mil': 1388.0,
                                         'extensao_rede_km': 13170.0,
                                         'indice_atendimento_percentual': 0.635,
                                         'indice_atendimento_tratado_percentual': 0.591,
                                         'ligacoes_mil': 1222.0,
                                         'populacao_atendida_mil': 3763.0,
                                         'volume_faturado_mil_m3': 40437.0,
                                         'volume_tratado_mil_m3': 37472.0},
                           'indice_perda_agua': 28.77,
                           'investimentos': {   'agua': 18059,
                                                'esgoto': 22635,
                                                'total': 43328},
                           'periodo': '12M'}},
    '2021': {   '12M': {   'agua': {   'economias_mil': 2485.0,
                                       'extensao_rede_km': 31386.0,
                                       'indice_atendimento_percentual': 0.975,
                                       'ligacoes_mil': 2285.0,
                                       'populacao_atendida_mil': 5851.0,
                                       'volume_faturado_mil_m3': 68176.0,
                                       'volume_produzido_mil_m3': 95552.0},
                           'ano': 2021,
                           'esgoto': {   'economias_mil': 1450.0,
                                         'extensao_rede_km': 13662.0,
                                         'indice_atendimento_percentual': 0.655,
                                         'indice_atendimento_tratado_percentual': 0.611,
                                         'ligacoes_mil': 1283.0,
                                         'populacao_atendida_mil': 3932.0,
                                         'volume_faturado_mil_m3': 42562.0,
                                         'volume_tratado_mil_m3': 39551.0},
                           'indice_perda_agua': 26.72,
                           'investimentos': {   'agua': 19357,
                                                'esgoto': 12508,
                                                'total': 37746},
                           'periodo': '12M'}},
    '2022': {   '12M': {   'agua': {   'economias_mil': 2544.0,
                                       'extensao_rede_km': 32431.0,
                                       'indice_atendimento_percentual': 0.9773,
                                       'ligacoes_mil': 2346.0,
                                       'populacao_atendida_mil': 5941.0,
                                       'volume_faturado_mil_m3': 69773.0,
                                       'volume_produzido_mil_m3': 96061.0},
                           'ano': 2022,
                           'esgoto': {   'economias_mil': 1519.0,
                                         'extensao_rede_km': 14817.0,
                                         'indice_atendimento_percentual': 0.6761,
                                         'indice_atendimento_tratado_percentual': 0.61,
                                         'ligacoes_mil': 1351.0,
                                         'populacao_atendida_mil': 4110.0,
                                         'volume_faturado_mil_m3': 44506.0,
                                         'volume_tratado_mil_m3': 41682.0},
                           'indice_perda_agua': 27.37,
                           'investimentos': {   'agua': 13990,
                                                'esgoto': 11090,
                                                'total': 49200},
                           'periodo': '12M'}},
    '2023': {   '12M': {   'agua': {   'economias_mil': 2588.0,
                                       'extensao_rede_km': 32680.0,
                                       'indice_atendimento_percentual': 0.9785,
                                       'ligacoes_mil': 2387.0,
                                       'populacao_atendida_mil': 5993.0,
                                       'volume_faturado_mil_m3': 71719.0,
                                       'volume_produzido_mil_m3': 96694.0},
                           'ano': 2023,
                           'esgoto': {   'economias_mil': 1616.0,
                                         'extensao_rede_km': 16236.0,
                                         'indice_atendimento_percentual': 0.7141,
                                         'indice_atendimento_tratado_percentual': 0.63,
                                         'ligacoes_mil': 1439.0,
                                         'populacao_atendida_mil': 4373.0,
                                         'volume_faturado_mil_m3': 47554.0,
                                         'volume_tratado_mil_m3': 44498.0},
                           'indice_perda_agua': 25.72,
                           'investimentos': {   'agua': 61361,
                                                'esgoto': 10640,
                                                'total': 121244},
                           'periodo': '12M'}},
    '2024': {   '12M': {   'agua': {   'economias_mil': 2657.0,
                                       'extensao_rede_km': 33269.0,
                                       'indice_atendimento_percentual': 0.9806,
                                       'ligacoes_mil': 2448.0,
                                       'populacao_atendida_mil': 6078.0,
                                       'volume_faturado_mil_m3': 76676.0,
                                       'volume_produzido_mil_m3': 102866.0},
                           'ano': 2024,
                           'esgoto': {   'economias_mil': 1693.0,
                                         'extensao_rede_km': 16471.0,
                                         'indice_atendimento_percentual': 0.7342,
                                         'indice_atendimento_tratado_percentual': 0.64,
                                         'ligacoes_mil': 1507.0,
                                         'populacao_atendida_mil': 4551.0,
                                         'volume_faturado_mil_m3': 51655.0,
                                         'volume_tratado_mil_m3': 48880.0},
                           'indice_perda_agua': 24.82,
                           'investimentos': {   'agua': 168924,
                                                'esgoto': 21351,
                                                'total': 228328},
                           'periodo': '12M'}}}

# Dados originais fixos para 2019 (usado na restauração)
DADOS_ORIGINAIS_2019 = {
    "12M": {
        "periodo": "12M", "ano": 2019,
        "agua": {
            "populacao_atendida_mil": 5737.64147,
            "indice_atendimento_percentual": 0.971666086059657,
            "ligacoes_mil": 2209.858, "economias_mil": 2404.565,
            "extensao_rede_km": 30554.63917,
            "volume_faturado_mil_m3": 272938,
            "volume_produzido_mil_m3": 382166
        },
        "esgoto": {
            "populacao_atendida_mil": 3701.13063,
            "indice_atendimento_percentual": 0.626784153665151,
            "indice_atendimento_tratado_percentual": 0.931132925425875,
            "ligacoes_mil": 1201.067, "economias_mil": 1360.312,
            "extensao_rede_km": 13163.15257,
            "volume_faturado_mil_m3": 161741,
            "volume_tratado_mil_m3": 150731
        },
        "investimentos": {"agua": 91829, "esgoto": 76335, "total": 168164},
        "indice_perda_agua": 28.58
    },
    "9M": {
        "periodo": "9M", "ano": 2019,
        "agua": {
            "populacao_atendida_mil": 5713.96919,
            "indice_atendimento_percentual": 0.97,
            "ligacoes_mil": 2192.83, "economias_mil": 2393.851,
            "extensao_rede_km": 30514.00106,
            "volume_faturado_mil_m3": 200324.138,
            "volume_produzido_mil_m3": 289736.0155
        },
        "esgoto": {
            "populacao_atendida_mil": 3636.29589,
            "indice_atendimento_percentual": 0.617,
            "indice_atendimento_tratado_percentual": 0.574,
            "ligacoes_mil": 1178.01, "economias_mil": 1342.886,
            "extensao_rede_km": 12899.33314,
            "volume_faturado_mil_m3": 119817.389,
            "volume_tratado_mil_m3": 111038.260495
        },
        "investimentos": {"agua": 68871.75, "esgoto": 57251.25, "total": 126123},
        "indice_perda_agua": 30.86
    },
    "6M": {
        "periodo": "6M", "ano": 2019,
        "agua": {
            "populacao_atendida_mil": 5694.22797,
            "indice_atendimento_percentual": 0.97,
            "ligacoes_mil": 2177.426, "economias_mil": 2378.757,
            "extensao_rede_km": 30398.69769,
            "volume_faturado_mil_m3": 130045.899,
            "volume_produzido_mil_m3": 188428.7724
        },
        "esgoto": {
            "populacao_atendida_mil": 3578.11678,
            "indice_atendimento_percentual": 0.609,
            "indice_atendimento_tratado_percentual": 0.566,
            "ligacoes_mil": 1158.198, "economias_mil": 1322.88,
            "extensao_rede_km": 12881.25967,
            "volume_faturado_mil_m3": 78065.246,
            "volume_tratado_mil_m3": 72279.0553527
        },
        "investimentos": {"agua": 45914.5, "esgoto": 38167.5, "total": 84082},
        "indice_perda_agua": 30.98
    },
    "3M": {
        "periodo": "3M", "ano": 2019,
        "agua": {
            "populacao_atendida_mil": 5674.67844,
            "indice_atendimento_percentual": 0.97,
            "ligacoes_mil": 2162.502, "economias_mil": 2364.109,
            "extensao_rede_km": 30287.93859,
            "volume_faturado_mil_m3": 65384.091,
            "volume_produzido_mil_m3": 93029.90915
        },
        "esgoto": {
            "populacao_atendida_mil": 3536.15075,
            "indice_atendimento_percentual": 0.604,
            "indice_atendimento_tratado_percentual": 0.561,
            "ligacoes_mil": 1143.579, "economias_mil": 1308.054,
            "extensao_rede_km": 12853.04076,
            "volume_faturado_mil_m3": 38994.815,
            "volume_tratado_mil_m3": 36071.5428921
        },
        "investimentos": {"agua": 22957.25, "esgoto": 19083.75, "total": 42041},
        "indice_perda_agua": 29.72
    }
}

@app.route("/api/inserir_dados", methods=["POST"])
def inserir_dados():
    """Insere ou atualiza dados operacionais"""
    try:
        novo_dado = request.get_json()
        campos_obrigatorios = ["ano", "periodo", "agua", "esgoto", "investimentos", "indice_perda_agua"]
        
        if not novo_dado or not all(key in novo_dado for key in campos_obrigatorios):
            return jsonify({
                "error": "Dados incompletos. Certifique-se de enviar ano, periodo, agua, esgoto, investimentos e indice_perda_agua."
            }), 400

        # Verificar se já existe um registro para o ano e período
        existing_record = collection_operacional.find_one({
            "ano": novo_dado["ano"], 
            "periodo": novo_dado["periodo"]
        })
        
        if existing_record:
            collection_operacional.update_one(
                {"ano": novo_dado["ano"], "periodo": novo_dado["periodo"]},
                {"$set": novo_dado}
            )
            return jsonify({
                "message": f"Dados para o ano {novo_dado['ano']} ({novo_dado['periodo']}) atualizados com sucesso!"
            }), 200

        # Inserir novo registro
        collection_operacional.insert_one(novo_dado)
        return jsonify({
            "message": f"Dados para o ano {novo_dado['ano']} ({novo_dado['periodo']}) inseridos com sucesso!"
        }), 201

    except Exception as e:
        app.logger.error(f"Erro ao inserir dados: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/limpar_dados_inseridos", methods=["POST"])
def limpar_dados_inseridos():
    """Remove todos os registros de 2025 em diante"""
    try:
        result = collection_operacional.delete_many({
            "$and": [
                {"ano": {"$gte": 2025}}, 
                {"periodo": {"$in": ["3M", "6M", "9M", "12M"]}}
            ]
        })
        return jsonify({
            "message": f"{result.deleted_count} registros inseridos manualmente foram removidos."
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao limpar dados: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/restaurar_dados_originais", methods=["POST"])
def restaurar_dados_originais():
    """Restaura dados originais para um ano e período específico"""
    try:
        data = request.get_json()
        ano = data.get("ano")
        periodo = data.get("periodo")
        
        if not ano or not periodo:
            return jsonify({"error": "Ano ou período inválido ou não fornecido."}), 400

        # Se o ano for 2019, usar os dados fixos
        if ano == 2019:
            if periodo not in DADOS_ORIGINAIS_2019:
                return jsonify({
                    "error": f"Período {periodo} não disponível para o ano 2019."
                }), 400
            original_data = DADOS_ORIGINAIS_2019[periodo]
        elif ano in DADOS_ORIGINAIS_COMPLETOS and periodo in DADOS_ORIGINAIS_COMPLETOS[str(ano)]:
            original_data = DADOS_ORIGINAIS_COMPLETOS[str(ano)][periodo]
        else:
            # Buscar o registro original mais antigo para outros anos
            original_record = collection_operacional.find_one(
                {"ano": ano, "periodo": periodo}, 
                sort=[("_id", 1)]
            )
            if not original_record:
                return jsonify({
                    "error": f"Nenhum registro original encontrado para o ano {ano} e período {periodo}."
                }), 404
            original_data = original_record

        # Atualizar ou inserir o registro
        existing_record = collection_operacional.find_one({"ano": ano, "periodo": periodo})
        if existing_record:
            collection_operacional.update_one(
                {"ano": ano, "periodo": periodo},
                {"$set": original_data}
            )
        else:
            collection_operacional.insert_one(original_data)
            
        return jsonify({
            "message": f"Dados originais restaurados para o ano {ano} ({periodo})."
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao restaurar dados: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/deletar_dados", methods=["POST"])
def deletar_dados():
    """Deleta dados específicos por ano e período"""
    try:
        data = request.get_json()
        ano = data.get("ano")
        periodo = data.get("periodo")
        
        if not ano or not periodo:
            return jsonify({"error": "Ano ou período inválido ou não fornecido."}), 400

        result = collection_operacional.delete_one({"ano": ano, "periodo": periodo})
        if result.deleted_count == 0:
            return jsonify({
                "error": f"Nenhum registro encontrado para o ano {ano} e período {periodo}."
            }), 404

        return jsonify({
            "message": f"Dados do ano {ano} ({periodo}) deletados com sucesso!"
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao deletar dados: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/dados_historicos", methods=["GET"])
def dados_historicos():
    """Retorna dados históricos para um período específico"""
    try:
        periodo = request.args.get("periodo", "12M")
        if periodo not in ["3M", "6M", "9M", "12M"]:
            return jsonify({"error": "Período inválido."}), 400

        # Buscar os dados mais recentes para cada ano e período especificado
        pipeline = [
            {"$match": {"periodo": periodo}},
            {"$sort": {"ano": 1, "_id": -1}},
            {
                "$group": {
                    "_id": "$ano",
                    "doc": {"$first": "$$ROOT"}
                }
            },
            {"$replaceRoot": {"newRoot": "$doc"}},
            {"$sort": {"ano": 1}}
        ]
        
        dados = list(collection_operacional.aggregate(pipeline))
        if not dados:
            return jsonify({"error": f"Nenhum dado encontrado para {periodo}."}), 404

        df_op = pd.DataFrame(dados)
        df_op["agua_cobertura"] = df_op["agua"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
        df_op["esgoto_cobertura"] = df_op["esgoto"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
        df_op["populacao"] = df_op["agua"].apply(lambda x: x.get("populacao_atendida_mil", 100)) * 1000
        df_op["ano"] = df_op["ano"].astype(int)

        return jsonify({
            "anos": df_op["ano"].tolist(),
            "periodos": df_op["periodo"].tolist(),
            "agua_cobertura": df_op["agua_cobertura"].round(2).tolist(),
            "esgoto_cobertura": df_op["esgoto_cobertura"].round(2).tolist(),
            "populacao": df_op["populacao"].round(0).tolist()
        })

    except Exception as e:
        app.logger.error(f"Erro ao buscar dados históricos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/modelo_regressao", methods=["GET"])
def modelo_regressao():
    """Gera modelo de regressão linear para água e esgoto"""
    try:
        periodo = request.args.get("periodo", "12M")
        if periodo not in ["3M", "6M", "9M", "12M"]:
            return jsonify({"error": "Período inválido. Use 3M, 6M, 9M ou 12M."}), 400

        df_op = pd.DataFrame(list(collection_operacional.find({"periodo": periodo})))
        if df_op.empty:
            return jsonify({
                "error": f"Nenhum dado operacional encontrado para o período {periodo}."
            }), 404

        # Preparação dos dados
        df_op["agua_cobertura"] = df_op["agua"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
        df_op["esgoto_cobertura"] = df_op["esgoto"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
        df_op["invest_agua"] = df_op["investimentos"].apply(lambda x: x.get("agua", 0)) / 1000000
        df_op["invest_esgoto"] = df_op["investimentos"].apply(lambda x: x.get("esgoto", 0)) / 1000000
        df_op["populacao"] = df_op["agua"].apply(lambda x: x.get("populacao_atendida_mil", 100)) * 1000
        df_op["ano"] = df_op["ano"].astype(int)
        df_op = df_op.dropna()

        # Criação dos modelos
        modelo_agua = LinearRegression().fit(
            df_op[["ano", "invest_agua", "populacao"]], 
            df_op["agua_cobertura"]
        )
        modelo_esgoto = LinearRegression().fit(
            df_op[["ano", "invest_esgoto", "populacao"]], 
            df_op["esgoto_cobertura"]
        )

        return jsonify({
            "modelo_agua": {
                "coeficientes": modelo_agua.coef_.tolist(),
                "intercepto": modelo_agua.intercept_,
                "explicacao": {
                    "ano": "Aumento na cobertura de água (%) por ano",
                    "invest_agua": "Aumento na cobertura de água (%) por milhão de reais investido",
                    "populacao": "Aumento na cobertura de água (%) por habitante"
                }
            },
            "modelo_esgoto": {
                "coeficientes": modelo_esgoto.coef_.tolist(),
                "intercepto": modelo_esgoto.intercept_,
                "explicacao": {
                    "ano": "Aumento na cobertura de esgoto (%) por ano",
                    "invest_esgoto": "Aumento na cobertura de esgoto (%) por milhão de reais investido",
                    "populacao": "Aumento na cobertura de esgoto (%) por habitante"
                }
            }
        })

    except Exception as e:
        app.logger.error(f"Erro no modelo de regressão: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/simulacao_investimento", methods=["POST"])
def simulacao_investimento():
    """Simula investimentos futuros baseado em metas"""
    try:
        data = request.get_json()
        anos_futuros = data.get("anos_futuros", list(range(2025, 2041)))
        meta_agua = float(data.get("meta_agua", 99.0))
        meta_esgoto = float(data.get("meta_esgoto", 90.0))
        meta_perda = float(data.get("meta_perda", 25.0))
        invest_agua_custom = data.get("invest_agua", [])
        invest_esgoto_custom = data.get("invest_esgoto", [])
        periodo_base = data.get("periodo_base", "12M")

        if invest_agua_custom and invest_esgoto_custom:
            if len(anos_futuros) != len(invest_agua_custom) or len(anos_futuros) != len(invest_esgoto_custom):
                return jsonify({
                    "error": "Os arrays de investimentos devem ter o mesmo tamanho que os anos futuros."
                }), 400

        # Ajuste para período
        periodos_em_meses = {"3M": 3, "6M": 6, "9M": 9, "12M": 12}
        meses_periodo = periodos_em_meses.get(periodo_base, 12)
        fator_ajuste = meses_periodo / 12

        # Preparação dos dados históricos
        df_op = pd.DataFrame(list(collection_operacional.find({"periodo": periodo_base})))
        if df_op.empty:
            return jsonify({
                "error": f"Nenhum dado operacional encontrado para o período {periodo_base}."
            }), 404

        df_op["agua_cobertura"] = df_op["agua"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
        df_op["esgoto_cobertura"] = df_op["esgoto"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
        df_op["invest_agua"] = df_op["investimentos"].apply(lambda x: x.get("agua", 0)) * fator_ajuste / 1e6
        df_op["invest_esgoto"] = df_op["investimentos"].apply(lambda x: x.get("esgoto", 0)) * fator_ajuste / 1e6
        df_op["populacao"] = df_op["agua"].apply(lambda x: x.get("populacao_atendida_mil", 100)) * 1000
        df_op["ano"] = df_op["ano"].astype(int)
        df_op = df_op.dropna()

        # Criação dos modelos
        modelo_agua = LinearRegression().fit(
            df_op[["ano", "invest_agua", "populacao"]], 
            df_op["agua_cobertura"]
        )
        modelo_esgoto = LinearRegression().fit(
            df_op[["ano", "invest_esgoto", "populacao"]], 
            df_op["esgoto_cobertura"]
        )

        # Simulação para anos futuros
        anos_proj = []
        cobertura_agua = []
        cobertura_esgoto = []
        investimentos_agua = []
        investimentos_esgoto = []

        for i, ano in enumerate(anos_futuros):
            # Projeção de população (crescimento de 1% ao ano)
            populacao_proj = df_op["populacao"].iloc[-1] * (1.01 ** (ano - df_op["ano"].iloc[-1]))

            # Verificar se há investimentos customizados
            if invest_agua_custom and invest_esgoto_custom and i < len(invest_agua_custom) and i < len(invest_esgoto_custom):
                if invest_agua_custom[i] is not None and invest_esgoto_custom[i] is not None:
                    inv_agua = float(invest_agua_custom[i]) / 1e6
                    inv_esgoto = float(invest_esgoto_custom[i]) / 1e6
                else:
                    # Cálculo automático de investimento
                    inv_agua = max((meta_agua - modelo_agua.predict([[ano, 0, populacao_proj]])[0]) / 10, 0)
                    inv_esgoto = max((meta_esgoto - modelo_esgoto.predict([[ano, 0, populacao_proj]])[0]) / 10, 0)
            else:
                # Cálculo automático de investimento
                inv_agua = max((meta_agua - modelo_agua.predict([[ano, 0, populacao_proj]])[0]) / 10, 0)
                inv_esgoto = max((meta_esgoto - modelo_esgoto.predict([[ano, 0, populacao_proj]])[0]) / 10, 0)

            # Predições de cobertura
            pred_agua = modelo_agua.predict([[ano, inv_agua, populacao_proj]])[0]
            pred_esgoto = modelo_esgoto.predict([[ano, inv_esgoto, populacao_proj]])[0]

            anos_proj.append(ano)
            cobertura_agua.append(round(min(pred_agua, 100), 2))
            cobertura_esgoto.append(round(min(pred_esgoto, 100), 2))
            investimentos_agua.append(round(inv_agua * 1e6 / fator_ajuste, 2))
            investimentos_esgoto.append(round(inv_esgoto * 1e6 / fator_ajuste, 2))

        # Predição de perdas (simplificada)
        perda_prevista = [min(meta_perda, 30)] * len(anos_futuros)

        return jsonify({
            "anos": anos_proj,
            "proj_agua_cobertura": cobertura_agua,
            "proj_esgoto_cobertura": cobertura_esgoto,
            "invest_agua": investimentos_agua,
            "invest_esgoto": investimentos_esgoto,
            "perdas_previstas": perda_prevista,
            "meta_agua": meta_agua,
            "meta_esgoto": meta_esgoto,
            "meta_perda": meta_perda
        })

    except Exception as e:
        app.logger.error(f"Erro na simulação de investimento: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    """Página inicial da API"""
    return jsonify({
        "message": "API Smart Saneamento está funcionando!",
        "endpoints": [
            "/api/dados_historicos",
            "/api/inserir_dados",
            "/api/limpar_dados_inseridos",
            "/api/restaurar_dados_originais",
            "/api/deletar_dados",
            "/api/modelo_regressao",
            "/api/simulacao_investimento"
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

