'''
    PUCPR - Tecnologia em Big Data e Inteligência Analítica - Inverno 2022

    Descrição   : Código fonte para jogo ZombieDice, projeto de Raciocíno Computacional.
    Tutor       : Professor Galbas
    Aluno       : Giovani Drosda Lima | gdrosdalima@gmail.com

'''

# Bibliotecas

from operator import countOf
import time, random, copy
import modules.md_UiFunctions as UI, modules.md_CharacterControl as CC

#--

UI.defineModes()

'''

Welcome: mensagem de boas vindas

'''
def Welcome():
    UI.speech('ATENÇÃO: este programa usa alguns caracteres UTF-8. Caso seu console não esteja configurado com suporte UTF-8,', .01)
    UI.speech('\n vão aparecer uns bagulhos sinistros na tela.', .01)
    UI.speech('\nAqui uma demonstração desses caracteres: ⣿⣿⣿', .01)
    UI.speech('\nPS: o console do VScode decodifica estes caracteres ^^, o CMD do Windows normalmente não.', .01)
    UI.speech('\nPS²: Caso esteja testando o jogo, é possível utilizar os nomes chuck norris e hackerman para ficar com a quantidade total de cérebros após a 1ª rodada. (use um para cada jogador para testar o desempate)', .01)
    UI.newSection()
    time.sleep(5)
    UI.newSection()
    UI.speech("Olá! Bem vindos ao ZombieDice.\n", .04)
    time.sleep(2)
    UI.speech("Este é um jogo de zumbi, mas antes que você comece a se gabar\n", .01)
    UI.speech("de ser um expert em sobrevivência pós-apocalíptica porque já\n", .01)
    UI.speech("assistiu todas as temporadas de The Walking Dead, fique sabendo que:", .01)
    time.sleep(2)
    UI.speech("\n\n   1. Já pode tirar seu cavalinho da horda de zumbis, Rick Grimes.", .01)
    UI.speech("\n      Neste jogo, VOCÊ É O ZUMBI.", .01)
    time.sleep(1)
    UI.speech("\n\n   2. Para de ser fanboy, aceita logo que TWD fica paia depois da 6 temporada :/", .01)
    time.sleep(3)

    UI.speech("\n\nOk, preparem a pipoca, acomodem-se na cadeira, abram o suco de tamarindo (com sabor de limão)!", .01)
    UI.speech("\nVamos começar. Antes, eu preciso saber quanta gente vai jogar.", .01)
    UI.speech("\nAh, e não se preocupe se tiver pouca gente! Posso usar meus poderes", .01)
    UI.speech("\npsiônicos para invocar uns bots.", .01)

    StartMenu()
#enddef

'''

StartMenu: Define a quantidade de jogadores e de bots

'''

def StartMenu():
    while True:
        try:
            quantityOfPlayers = int(input("\nQuantas pessoas vão jogar?:"))
            if quantityOfPlayers < 0:
                quantityOfPlayers *= -1

            break
        except ValueError:
            print("Oops... Algo deu errado. Você inseriu um número de jogadores?")
    #endwhile    

    print("Entendi, {} pessoas vão jogar.".format(quantityOfPlayers))

    while True:
        try:
            quantityOfBots = int(input("\nQuantos bots vão jogar?:"))
            if quantityOfBots < 0:
                quantityOfBots *= -1

            break
        except ValueError:
            print("Oops... Algo deu errado. Você inseriu um número de bots?")
    #endwhile   
      
    print("Bip bop, {} bots vão jogar.".format(quantityOfBots))

    TotalInThisGame = CC.TotalInGame(quantityOfPlayers, quantityOfBots)

    if TotalInThisGame.total <= 1:
        UI.speech("\n\nQuer todos os cérebros pra você? ~.o", .03)
        UI.speech("\nAdicione pelo menos 2 jogadores ou bots para iniciar.\n", .03)
        StartMenu()

    if TotalInThisGame.players == 0:
        print("Robô também sofre, abaixem o preço do i9!")

    PlayersInGame = CC.SetCharacters(TotalInThisGame)
    UI.ScriptStartGame(PlayersInGame)
    StartGame(PlayersInGame)

#enddef


'''

'''
def thankYou():
    UI.newSection()
    UI.speech('\nObrigado por jogar minha versão de ZombieDice.\n', .03)
    UI.speech('Espero que tenha se divertido o tanto quanto eu me diverti fazendo ele (ou mais!)\n', .03)
    UI.speech('De fato, gostei tanto de construir ele, que vou aprimorar a jogatina.\n', .03)
    UI.speech('Lembra quando tu foi definir seu personagem e lá dizia que tinha classes em construção?\n', .03)
    UI.speech('Pois é.\n', .03)
    UI.speech('E o melhor, tá tudo open source no GitHub...\n', .03)
    UI.speech('https://github.com/dlgiovani\n', .03)
    UI.speech('\n-- Obrigado ao prof Galbas por lecionar a matéria de RC com tanta qualidade\n', .03)

'''

StartGame: inicia as rodadas

'''

def StartGame(PlayersInGame):
    UI.newSection()
    keepPlaying = 's'
    hasWinner   = False

    while not hasWinner:

        CC.play(PlayersInGame)

        for p in PlayersInGame:
            '''
            Use estes nomes para testar as condições de desempate e vitória mais facilmente.
            '''
            if p['name'].lower() in ('chuck norris', 'hackerman'):
                p['brains'] = CC.Klass[p['klass']]['fullBelly']

            if p['brains'] == CC.Klass[p['klass']]['fullBelly']:
                hasWinner = True


        if hasWinner:
            winnerPlayer = CC.tiebreak(PlayersInGame)
            CC.congratulateWinner(winnerPlayer)
            thankYou()

#enddef

Welcome()