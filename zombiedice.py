'''
    PUCPR - Tecnologia em Big Data e Inteligência Analítica - Inverno 2022

    Descrição   : Código fonte standalone para jogo ZombieDice, projeto de Raciocíno Computacional.
    Tutor       : Professor Galbas
    Aluno       : Giovani Drosda Lima | gdrosdalima@gmail.com

'''

# Bibliotecas

import time, random, copy

#--

# definição de classes, dicionários e afins [INÍCIO]

class Player:
    def __init__(info, name, description, klass, isBot, hp, brains):
        info.name           = name
        info.description    = description
        info.klass          = Klass[klass][0]
        info.isBot          = isBot
        info.hp             = hp
        info.brains         = 0
        info.itemQty        = Klass[klass][1]
    #enddef
#endclass

class TotalInGame:
    def __init__(qtd, qtdplayers, qtdbots):
        qtd.players = qtdplayers
        qtd.bots    = qtdbots
        qtd.total   = qtdplayers + qtdbots
    #enddef
#endclass

Klass = {
    1: ["Parrudo", 0, "Enquanto as outras classes possuem 3 de vida, esta tem 4. Porém, devido ao seu acelerado metabolismo, precisa consumir 15 cérebros para a vitória ao invés de 13."],
    2: ["Incansável", 0, "Caso os 3 dados na rodada deste zumbi resultem em passos, este pode optar por correr mais um pouco e jogar mais um dado para tentar alcançar sua vítima."],
    3: ["Ciclista", 4, "Este zumbi já não anda mais de bicicleta, mas ainda tem um capacete que oferece 50% de chances de protegê-lo do tiro. Durabilidade de 4 tiros."],
    4: ["Cowboy", 0, "Se o cowboy conseguir cérebros na rodada, ele pode optar por trocá-los por laços. Ao jogar um laço, existe 30% de chances de pegar 1 vítima, 15% de pegar 2 e 3% de pegar 3."]
}

BotNameSyllables    = {"kan", "len", "ghi", "flok", "trom", "fle", "dros", "da", "li", "ma"}
BotGenerationMessages      = {
    "Mordendo uns transeuntes...",
    "Selecionando os melhores cérebros...",
    "Fazendo uma pausa pro lanche...",
    "Costurando mandíbulas tortas...",
    "Enchendo linguiça...",
    "Treinando o zumbi...",
    "Enchendo a caneca de café..."
}

PlayersInGame = []

# definição de classes, dicionários e afins [FIM]

def newSection():
    print("\n\n")
    print("===========================================")
    print("###########################################")
    print("===========================================")
    print("\n\n")

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

    TotalInGame(quantityOfPlayers, quantityOfBots)

    if TotalInGame.total <= 1:
        print("Quer todos os cérebros pra você? ~.o")
        print("Adicione pelo menos 2 jogadores ou bots para iniciar.")
        StartMenu()

    if TotalInGame.qtdplayers == 0:
        print("Robô também sofre, abaixem o preço do i9!")

    
    SetCharacters()

#enddef

def SetCharacters():
    newSection()
    GenerateBots()

    newSection()
    SetPlayers()

#enddef

def GenerateBots(quantityOfBots):
    print("Ok! vou gerar os bots...\n")

    for x in range(random.randint(3, 6)):
        print(random.choice(list(BotGenerationMessages))) #imersão
        time.sleep(2)

    print("") #linebreak
    for i in range(quantityOfBots):

        quantityOfSyllables = random.choice([2,3])
        name = ''
        
        for o in range(quantityOfSyllables):
            name += random.choice(tuple(BotNameSyllables))
            
        description = 'bipbop' #TODO add cool descriptions
        klass = random.choice(list(Klass))
        isBot = True

        PlayersInGame.append(str(Player(name, description, klass, isBot, 3, 0).__dict__))

        print("Nasce {}, um zumbi {}!".format(name, Klass[klass][0]))

#enddef


def SetPlayers():
    print("Joia. Agora, vamos criar os personagens dos jogadores ^ü^ eba!")

    name = input("Escolha um nome que faça jus à grandeza de seu personagem:")
    print("{}! Que nome digno!".format(name))

    print("Vamos escolher a classe do seu personagem.")
    for x in Klass:
        print("{}. {} - {}".format(x,Klass[x][0],Klass[x][2]))

SetPlayers()