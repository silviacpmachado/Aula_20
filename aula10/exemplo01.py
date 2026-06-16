# python -m venv venv
# source ./venv/Scripts/activate
# pip install pandas numpy
# pip install matplotlib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 


# obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # iso-8859-1  | utf-8  | latin1 | cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]

    # agrupando e quantificando as variáveis quantitativa
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    # ordenando em decrescente:
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)
    
    # print(df_roubo_veiculo)

except Exception as e:
    print(f'Erro ao obter os dados: {e}')
    exit()


# Obtendo informações
try:
    print('Obtendo informações a cerca dos roubos de veículos... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)


    print('\nMedidas de tendência Central')
    print(40*'=')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância ente média e mediana: {distancia}%')


    # Obtendo os quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25)
    q2 = np.quantile(array_roubo_veiculo, 0.50)
    q3 = np.quantile(array_roubo_veiculo, 0.75)

    print('\nMedidas de Posição')
    print(40*'=')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')


    # menores
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

    # maiores
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]
    
    print('\nMunicípios com Mais Roubos')
    print(40*'=')
    print(df_roubo_veiculo_maiores)

    print('\nMunicípios com Menos Roubos')
    print(40*'=')
    # ordem decrescente
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

except Exception as e:
    print(f'Erro ao calcular as informações...')


# Medidas de Dispersão - Amplitude Total
try:
    # Amplitude Total = maior_valor - menor_valor
    # Quanto mais próximo de zero, maior a homogeneidade dos dados
    # Se for igual a 0, todos os dados são iguais
    # Quanto mais próximo do maior valor, maior a dispersão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(40*'=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medida de dispersão {e}')


# Outliers
try:
#   IQR (Intervalo Interquartil)
#   É a amplitude dos 50% dos dados mais centrais
#   IQR = q3 - q1
#   Ele ignora os valores mais extremos, max e min estão fora.
#   Não sofre influência dos extremos
#   Quanto mais próximo de zero, maior a homogeneidade dos dados
#   Se for igual a 0, todos os dados são iguais
#   Quanto mais próximo do Q3, maior a dispersão
    iqr = q3 - q1  # 969.5

    # print(f'\nIQR: {iqr}')

    # limite inferior
    limite_inferior = q1 - (1.5 * iqr)

    # limite superior
    limite_superior = q3 + (1.5 * iqr)


    # outliers
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
        
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print('\nMedidas:')
    print(40*'=')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')  # mediana
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')


    print('\nOutliers Superiores:')
    print(40*'=')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_superiores)


    print('\nOutliers Inferiores:')
    print(40*'=')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existe outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores)


except Exception as e:
    print(f'Erro ao calcular Outliers {e}')


# Visualizando os dados
try:
    # mostrando cidade com maiores roubos
    # plt.figure(figsize=(16, 8))
    plt.subplots(2, 2, figsize=(16, 8))

    # 1 Maiores
    plt.subplot(2, 2, 1)    
    df_roubo_veiculo_maiores = (
        df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False)
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=True)
    )
    plt.barh(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    plt.title('Cidades com maiores casos de roubos')


    # 2 Menores
    plt.subplot(2, 2, 2) 
    
    if len(df_roubo_veiculo_outliers_inferiores)>0:
        df_roubo_veiculo_outliers_inferiores = (df_roubo_veiculo_outliers_inferiores.sort_values(by='roubp_veiculo', ascending=True)
        )
        ply.barh(
            df_roubo_veiculo_outliers_inferiores['munic'],
            df_roubo_veiculo_outliers_inferiores['roubo_veiculo']
        )

        plt.title('Municípios com Outliers Inferiores')
    else:
        df_roubo_veiculo_menores = (
        df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True)
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=False)
        )


    plt.barh(
        df_roubo_veiculo_menores['munic'],
        df_roubo_veiculo_menores['roubo_veiculo']
        )
    plt.title('Cidades com menores casos de roubos')

    #POSIÇÃO 3 - BOXPLOT
    plt.subplot(2, 2, 3)

    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True) 




    plt.subplot(2, 2, 4) 



    plt.show()

except Exception as e:
    print(f'Erro ao plotar gráfico: {e}')

