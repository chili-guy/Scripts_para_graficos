import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importando o arquivo CSV
df = pd.read_csv("TESTE DE FLEXÃO.csv")

# Exibindo as colunas
print(df.columns)

df
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
n_porcentagens = len(porcentagens)
bar_width = 0.15  # Largura das barras

# Posições das barras
index = np.arange(len(temperaturas))

# Configurando a paleta de cores pastel
colors = sns.color_palette("pastel", n_porcentagens)

# Criando a figura
plt.figure(figsize=(10, 5))

# Plotando barras para cada concentração
for i, porcentagem in enumerate(porcentagens):
    medias = [resultados.loc[temp, porcentagem][0] for temp in temperaturas]
    desvios = [resultados.loc[temp, porcentagem][1] for temp in temperaturas]
    plt.bar(index + i * bar_width, medias, bar_width, yerr=desvios, capsize=5, label=f'{porcentagem}%', color=colors[i])

# Ajustando a legenda e os eixos
plt.xlabel('Temperatura (ºC)', fontsize=14)
plt.ylabel('Tensão (MPa)', fontsize=14)
plt.title('Tensão por Temperatura e Concentração', fontsize=16)
plt.xticks(index + (n_porcentagens - 1) * bar_width / 2, temperaturas, fontsize=12)  # Ajuste centralizado dos ticks do eixo x
plt.legend(title='Concentração', fontsize=12, title_fontsize='14')

# Ajustando o eixo Y para começar em zero
plt.ylim(0, None)

# Configurando o grid e estética
plt.grid(True, which='both', linestyle='-', linewidth=0.5, color='gray', alpha=0.4)

# Ajustes para estética acadêmica
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.gca().spines['right'].set_color('gray')
plt.gca().spines['right'].set_linewidth(1.2)
plt.gca().spines['top'].set_color('gray')
plt.gca().spines['top'].set_linewidth(1.2)
plt.gca().yaxis.set_ticks_position('left')
plt.gca().xaxis.set_ticks_position('bottom')

plt.tight_layout()  # Ajuste para evitar sobreposição
plt.show()
