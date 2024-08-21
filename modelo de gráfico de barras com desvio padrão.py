import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importando o arquivo CSV
df = pd.read_csv("TESTE DE FLEXÃO.csv")

# Exibindo as colunas
print(df.columns)

# Substituindo vírgulas por pontos (assumindo que as vírgulas são separadores decimais)
df['Tensão'] = df['Tensão'].str.replace(',', '.')

# Convertendo para float
df['Tensão'] = df['Tensão'].astype(float)

# Função para calcular a média e o desvio padrão
def calcular_media_desvio_padrao(dados):
    media = np.mean(dados)
    desvio_padrao = np.std(dados)
    return media, desvio_padrao

# Agrupando os dados por temperatura e concentração e calculando médias e desvios padrão
resultados = df.groupby(['Temperatura', 'Porcentagem'])['Tensão'].apply(calcular_media_desvio_padrao).unstack()

# Preparando para criar o gráfico
temperaturas = df['Temperatura'].unique()
porcentagens = df['Porcentagem'].unique()
n_temperaturas = len(temperaturas)
bar_width = 0.14  # Largura das barras

# Posições das barras
index = np.arange(len(porcentagens))

# Configurando a paleta de cores pastel
colors = sns.color_palette("pastel", n_temperaturas)

# Criando a figura
plt.figure(figsize=(10, 5))

# Plotando barras para cada temperatura
for i, temperatura in enumerate(temperaturas):
    medias = [resultados.loc[temperatura, conc][0] for conc in porcentagens]
    desvios = [resultados.loc[temperatura, conc][1] for conc in porcentagens]
    plt.bar(index + i * bar_width, medias, bar_width, yerr=desvios, capsize=5, label=f'{temperatura}ºC', color=colors[i])

# Ajustando a legenda e os eixos
plt.xlabel('Concentração (%)', fontsize=12)
plt.ylabel('Tensão (MPa)', fontsize=12)
plt.title('Tensão por Concentração e Temperatura', fontsize=12)
plt.xticks(index + (n_temperaturas - 1) * bar_width / 2, porcentagens, fontsize=10)  # Ajuste centralizado dos ticks do eixo x
plt.legend(title='Temperatura', fontsize=12, title_fontsize='12')

# Ajustando o eixo Y para começar em zero
plt.ylim(0, None)

# Configurando o grid e estética
plt.grid(True, which='both', linestyle='-', linewidth=0.5, color='gray', alpha=0.4)
plt.tight_layout()  # Ajuste para evitar sobreposição
plt.show()
