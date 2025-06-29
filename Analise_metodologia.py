# analise_de_metodologia.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

# Dados históricos

dates = [
    '2024-06-01', '2024-03-01', '2023-12-01', '2023-09-01', '2023-06-01', '2023-03-01',
    '2022-12-01', '2022-09-01', '2022-06-01', '2022-03-01', '2021-12-01', '2021-09-01',
    '2021-06-01', '2021-03-01', '2020-12-01', '2020-09-01', '2020-06-01', '2020-03-01',
    '2019-12-01', '2019-09-01', '2019-06-01', '2019-03-01'
]
index_values = [
    0.7362, 0.7342, 0.7333, 0.7257, 0.7206, 0.7140, 0.7073, 0.6908, 0.6838, 0.6761,
    0.6709, 0.6651, 0.6617, 0.6554, 0.6471, 0.6440, 0.6380, 0.6350, 0.6268, 0.6170,
    0.6090, 0.6040
]

# Criando o DataFrame

data = pd.DataFrame(data=index_values, index=pd.to_datetime(dates), columns=['Índice de Atendimento'])

# Extraindo variáveis independentes

data['Ano'] = data.index.year
data['Trimestre'] = data.index.quarter
data['Data_Ordinal'] = [date.toordinal() for date in data.index]
data['Data_Ordinal_Quadrado'] = data['Data_Ordinal'] ** 2

# Variável dependente categórica (1 se índice > 0.7, 0 caso contrário)

data['Acima_0_7'] = (data['Índice de Atendimento'] > 0.7).astype(int)

# Definindo features e target

X = data[['Ano', 'Trimestre', 'Data_Ordinal', 'Data_Ordinal_Quadrado']]
y_class = data['Acima_0_7']

# --- Regressão Logística ---
log_model = LogisticRegression(random_state=42)
log_model.fit(X, y_class)

# Projeção de datas futuras

future_dates = pd.date_range(start=data.index.min(), end='2030-12-31', freq='QE-DEC')
future_data = pd.DataFrame(index=future_dates)
future_data['Ano'] = future_data.index.year
future_data['Trimestre'] = future_data.index.quarter
future_data['Data_Ordinal'] = [date.toordinal() for date in future_data.index]
future_data['Data_Ordinal_Quadrado'] = future_data['Data_Ordinal'] ** 2

X_future = future_data[['Ano', 'Trimestre', 'Data_Ordinal', 'Data_Ordinal_Quadrado']]

log_prob = log_model.predict_proba(X_future)[:, 1]

print(f"Probabilidade de índice > 0.7 em dezembro de 2030: {log_prob[-1]*100:.2f}%")

# Plot logística

plt.figure(figsize=(12, 6))
plt.gca().set_facecolor('black')
plt.scatter(data.index, data['Índice de Atendimento'], c='cyan', s=50, label='Observado')
plt.axhline(0.7, linestyle='--', label='Limiar 0.7')
plt.axhline(0.9, linestyle='--', label='Meta 90%')
plt.axhline(1.0, linestyle='--', label='Meta 100%')
plt.plot(future_dates, log_prob, c='orange', label='LogReg Prob.')
plt.title('Regressão Logística: Probabilidade Índice > 0.7', color='white')
plt.xlabel('Ano', color='white')
plt.ylabel('Probabilidade', color='white')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('projecao_logistica.png')


# --- Árvore de Decisão ---
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(data[['Data_Ordinal']], data['Índice de Atendimento'])

# Projeção futura

dt_pred = dt_model.predict(pd.DataFrame({'Data_Ordinal': [date.toordinal() for date in future_dates]}, index=future_dates))

print(f"Índice projetado em 2030 (Tree): {dt_pred[-1]:.4f}")

# Plot árvore

plt.figure(figsize=(12, 6))
plt.gca().set_facecolor('black')
plt.scatter(data.index, data['Índice de Atendimento'], c='cyan', s=50, label='Observado')
plt.plot(future_dates, dt_pred, c='lime', label='Tree Pred')
plt.axhline(0.7, linestyle='--', label='Limiar 0.7')
plt.axhline(0.9, linestyle='--', label='Meta 90%')
plt.axhline(1.0, linestyle='--', label='Meta 100%')
plt.title('Árvore de Decisão: Projeção Índice Atendimento', color='white')
plt.xlabel('Ano', color='white')
plt.ylabel('Índice de Atendimento', color='white')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('projecao_arvore.png')


# --- Comparação de Modelos ---
# Instanciação de modelos
linear_model = LinearRegression()
# dt_model já instanciado acima
# log_model já instanciado acima

# Treinamento múltiplos modelos
linear_model.fit(X, data['Índice de Atendimento'])
# dt_model já treinado acima
log_model.fit(X, data['Acima_0_7'])

# Previsões futuras para os três modelos
linear_pred = linear_model.predict(X_future)
dt_pred_comp = dt_model.predict(pd.DataFrame({'Data_Ordinal': [date.toordinal() for date in future_dates]}, index=future_dates))
log_prob_comp = log_model.predict_proba(X_future)[:, 1]

print(f"Linear (2030): {linear_pred[-1]:.4f}")
print(f"Tree (2030): {dt_pred_comp[-1]:.4f}")
print(f"LogReg Prob >0.7 (2030): {log_prob_comp[-1]*100:.2f}%")

# Plot comparativo

plt.figure(figsize=(12, 6))
plt.gca().set_facecolor('black')
plt.scatter(data.index, data['Índice de Atendimento'], c='cyan', s=50, label='Observado')
plt.plot(future_dates, linear_pred, linestyle='--', label='Linear')
plt.plot(future_dates, dt_pred_comp, label='Tree')
plt.plot(future_dates, log_prob_comp, linestyle='-.', label='LogReg Prob')
plt.axhline(0.7, linestyle='--', label='Limiar 0.7')
plt.axhline(0.9, linestyle='--', label='Meta 90%')
plt.axhline(1.0, linestyle='--', label='Meta 100%')
plt.title('Comparação: Linear, Árvore e Logística', color='white')
plt.xlabel('Ano', color='white')
plt.ylabel('Índice / Probabilidade', color='white')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('comparacao_modelos.png')
