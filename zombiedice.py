'''
    PUCPR - Tecnologia em Big Data e Inteligência Analítica - Inverno 2022

    Descrição   : Código fonte standalone para jogo ZombieDice, projeto de Raciocíno Computacional.
    Tutor       : Professor Galbas
    Aluno       : Giovani Drosda Lima | gdrosdalima@gmail.com

'''

# Bibliotecas

import time, random

#--

# definição de classes, dicionários e afins [INÍCIO]

class Player:
    def __init__(info, name, description, klass, isBot, hp, brains, itemQty):
        info.name           = name
        info.description    = description
        info.klass          = Klass(klass)
        info.isBot          = isBot
        info.hp             = hp
        info.brains         = 0
        info.itemQty        = itemQty
    #enddef
#endclass

Klass = {
    "1": ["Parrudo", 1],
    "2": ["Veloz", 0],
    "3": ["Ciclista", 1],
    "4": ["Cowboy", 2]
}

BotNameSyllables = {"kan", "len", "ghi", "flok", "trom", "fle", "dros", "da", "li", "ma"}

# definição de classes, dicionários e afins [FIM]

def Welcome():
    print("Olá! Bem vindos ao ZombieDice.")
    time.sleep(2)
    print("Este é um jogo de zumbi, mas antes que você comece a se gabar")
    print("de ser um expert em sobrevivência pós-apocalíptica porque já")
    print("assistiu todas as temporadas de The Walking Dead, fique sabendo que:")
    time.sleep(7)
    print("\n   1. Já pode tirar seu cavalinho da horda de zumbis, Rick Grimes.")
    print("   Neste jogo, VOCÊ É O ZUMBI.")
    time.sleep(4)
    print("\n   2. Para de ser fanboy, aceita logo que TWD fica paia depois da 6 temporada :/")
    time.sleep(4)

    print("\nOk, preparem a pipoca, acomodem-se na cadeira, abram o refri!")
    print("Vamos começar. Antes, eu preciso saber quanta gente vai jogar.")
    print("Ah, e não se preocupe se tiver pouca gente! Dá pra chamar a turma")
    print("do seu Zumbnelson pra dar uma força (a.k.a. bots).")

    StartMenu()
#enddef

def StartMenu():
    while True:
        try:
            quantityOfPlayers = int(input("\nQuantas pessoas vão jogar?:"))
            break
        except ValueError:
            print("Oops... Algo deu errado. Você inseriu um número de jogadores?")
    #endwhile    

    print("Entendi, {} pessoas vão jogar.".format(quantityOfPlayers))

    while True:
        try:
            quantityOfBots = int(input("\nQuantos bots vão jogar?:"))
            break
        except ValueError:
            print("Oops... Algo deu errado. Você inseriu um número de bots?")
    #endwhile   
      
    print("Bip bop, {} bots vão jogar.".format(quantityOfBots))

    quantityOfPlayersAndBots = quantityOfPlayers + quantityOfBots

    if quantityOfPlayersAndBots <= 1:
        print("Quer todos os cérebros pra você? ~.o")
        print("Adicione pelo menos 2 jogadores ou bots para iniciar.")
        StartMenu()

    if quantityOfPlayers == 0:
        print("Robô também sofre, abaixem o preço do i9!")

    
    SetCharacters(quantityOfPlayers, quantityOfBots, quantityOfPlayersAndBots)

#enddef

def SetCharacters(quantityOfPlayers, quantityOfBots, quantityOfPlayersAndBots):
    for i in range(quantityOfBots):
        quantityOfSyllables = random.choice([2,3])
        name = ''
        
        for o in range(quantityOfSyllables):
            name += random.choice(tuple(BotNameSyllables))
        description = 'bipbop' #TODO add cool descriptions
        klass = random.choice(["1", "2", "3", "4"])
        isBot = True
        print("Nasce o grande {}, o zumbi {}".format(name, description))


StartMenu() #debbuging