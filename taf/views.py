from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'taf/home.html')

def resultado(request):
    idade = float(request.GET.get('idade_input'))
    
    tempo_corrida = float(request.GET.get('tempo_corrida_input').replace(':', '.'))

    tempo_shuttle = (0 if not request.GET.get('tempo_shuttle_input') else float(request.GET.get('tempo_shuttle_input')))

    n_flexoes_barra = (0 if not request.GET.get('n_flexoes_barra_input') else float(request.GET.get('n_flexoes_barra_input')))

    n_flexoes_solo = (0 if not request.GET.get('n_flexoes_solo_input') else float(request.GET.get('n_flexoes_solo_input')))

    n_abdominais = float(request.GET.get('n_abdominais_input'))
    
    notas = MediaGeral(idade, tempo_corrida, tempo_shuttle, n_flexoes_barra, n_flexoes_solo, n_abdominais)
    media_geral = notas['media_geral']
    situacao = ('Aprovado' if media_geral >= 6 else 'Reprovado')

    return render(request, 'taf/resultado.html', {
        'media_geral': media_geral,
        'situacao':situacao,
        'n1':notas['corrida'], 
        'n2':notas['shuttle'], 
        'n3':notas['flexoes_barra'], 
        'n4':notas['flexoes_solo'], 
        'n5':notas['abdominal']
        })



def CalcularNota(idade, indice):
    faixa_18_24 = [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0,
    ]

    faixa_25_29 = [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.0,
    ]

    faixa_30_34 = [
        0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.0, 10.0,
    ]

    faixa_35_39 = [
        0.0, 0.0, 0.0, 0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.0, 10.0, 10.0,
    ]

    faixa_40_44 = [
        0.0, 0.0, 0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0,
    ]

    faixa_45_49 = [
        0.0, 0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
    ]

    faixa_50 = [
        0.0,
        1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5,
        7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
    ]

    if idade <= 24:
        return faixa_18_24[indice]
    elif idade <= 29:
        return faixa_25_29[indice]
    elif idade <= 34:
        return faixa_30_34[indice]
    elif idade <= 39:
        return faixa_35_39[indice]
    elif idade <= 44:
        return faixa_40_44[indice]
    elif idade <= 49:
        return faixa_45_49[indice]
    else:
        return faixa_50[indice]


def NotaCorrida(idade, tempo):
    corrida = [
        22.21, 22.20, 21.20, 20.40, 19.50, 18.00, 17.10,
        16.20, 15.30, 14.40, 13.50, 13.00, 12.30, 12.00,
        11.30, 11.00, 10.30, 10.00, 9.45, 9.30, 9.15,
    ]

    indice = 0
    for i in range(21):
        if tempo <= corrida[i]:
            indice = i
        else:
            break

    return CalcularNota(idade, indice)

def NotaShuttle(idade, tempo):
    shuttle_run = [
        14.3, 14.1, 13.9, 13.7, 13.5, 13.3, 13.1,
        12.9, 12.7, 12.5, 12.3, 12.1, 11.9, 11.7,
        11.5, 11.3, 11.1, 10.9, 10.7, 10.5, 10.3,
    ]

    indice = 0
    for i in range(21):
        if tempo <= shuttle_run[i]:
            indice = i
        else:
            break

    return CalcularNota(idade, indice)


def NotaFlexaoBarra(idade, repeticoes):
    flexao_barra = [
        0, 0, 0, 0, 0, 0, 0,
        1, 2, 3, 4, 5, 6, 7,
        8, 9, 10, 11, 12, 13, 15
    ]

    indice = 0
    for i in range(21):
        if repeticoes >= flexao_barra[i]:
            indice = i
        else:
            break

    return CalcularNota(idade, indice)

def NotaFlexaoSolo(idade, repeticoes):
    flexao_solo = [
        8, 9, 10, 11, 12, 13, 14,
        16, 18, 20, 22, 24, 26, 28,
        30, 32, 34, 36, 38, 40, 42,
    ]

    indice = 0
    for i in range(21):
        if repeticoes >= flexao_solo[i]:
            indice = i
        else:
            break

    return CalcularNota(idade, indice)


def NotaAbdominal(idade, repeticoes):
    abdominal = [
        18, 19, 20, 21, 22, 23, 24,
        25, 26, 27, 28, 31, 32, 35,
        38, 41, 44, 47, 50, 53, 56,
    ]

    indice = 0
    for i in range(21):
        if repeticoes >= abdominal[i]:
            indice = i
        else:
            break

    return CalcularNota(idade, indice)

'''
4.5 Os avaliados, com idade igual ou inferior a 34 (trinta e quatro) anos, deverão executar
obrigatoriamente o teste de flexão de braço na barra fixa (masculino) e contração isométrica na barra
fixa (feminino), a corrida de 2400 m, o teste de shutlle run e o abdominal tipo remador;

4.6. Os avaliados com idade igual ou superior a 35 (trinta e cinco) anos até a idade igual ou
inferior a 49 (quarenta e nove) anos, poderão optar pela execução da flexão de braço no solo ou na
barra fixa (masculino) / contração isométrica na barra fixa (feminino), sendo vetada a execução das
duas atividades para este grupo. Executam os demais exercícios: a corrida de 2400 m, o teste de shutlle
run e o abdominal tipo remador;

4.7. Os avaliados com idade igual ou superior a 50 (cinquenta) anos deverão executar
obrigatoriamente a corrida de 2400 m, a flexão de braço sobre o solo e o abdominal tipo remador;

'''
def MediaGeral(idade, tempo_corrida, tempo_shutle, n_flexoes_barra, n_flexoes_solo, n_abdominais):
    nota_corrida = 0.0
    nota_shuttle = 0.0
    nota_flexoes_barra = 0.0
    nota_flexoes_solo = 0.0
    nota_abdominais = 0.0
    media_geral = 0.0

    if idade >= 50:
        nota_corrida = NotaCorrida(idade, tempo_corrida)
        nota_shuttle = 'Não se aplica'
        nota_flexoes_barra = 'Não se aplica'
        nota_flexoes_solo = NotaFlexaoSolo(idade, n_flexoes_solo)
        nota_abdominais = NotaAbdominal(idade, n_abdominais)
        media_geral = (nota_corrida + nota_flexoes_solo + nota_abdominais)/3

    elif idade > 34:
        if n_flexoes_barra == 0: #Optou por não realizar as flexões na barra
            nota_corrida = NotaCorrida(idade, tempo_corrida)
            nota_shuttle = NotaShuttle(idade, tempo_shutle)
            nota_flexoes_barra = 'Optou por não realizar o exercício'
            nota_flexoes_solo = NotaFlexaoSolo(idade, n_flexoes_solo)
            nota_abdominais = NotaAbdominal(idade, n_abdominais)
            media_geral = (nota_corrida + nota_shuttle + nota_flexoes_solo + nota_abdominais) / 4

        elif n_flexoes_solo == 0: #Optou por não realizar as flexões no solo
            nota_corrida = NotaCorrida(idade, tempo_corrida)
            nota_shuttle = NotaShuttle(idade, tempo_shutle)
            nota_flexoes_barra = NotaFlexaoBarra(idade, n_flexoes_barra)
            nota_flexoes_solo = 'Optou por não realizar o exercício'
            nota_abdominais = NotaAbdominal(idade, n_abdominais)
            media_geral = (nota_corrida + nota_shuttle + nota_flexoes_barra + nota_abdominais) / 4

    else: #Policiais com idade menor ou igual a 34 anos
        nota_corrida = NotaCorrida(idade, tempo_corrida)
        nota_shuttle = NotaShuttle(idade, tempo_shutle)
        nota_flexoes_barra = NotaFlexaoBarra(idade, n_flexoes_barra)
        nota_flexoes_solo = NotaFlexaoSolo(idade, n_flexoes_solo)
        nota_abdominais = NotaAbdominal(idade, n_abdominais)
        media_geral = (nota_corrida + nota_shuttle + nota_flexoes_barra + nota_flexoes_solo + nota_abdominais) / 5

    media_geral = round(media_geral, 3)

    notas = {
        'corrida': nota_corrida,
        'shuttle': nota_shuttle,
        'flexoes_barra': nota_flexoes_barra,
        'flexoes_solo': nota_flexoes_solo,
        'abdominal': nota_abdominais,
        'media_geral': media_geral
    }

    return notas



