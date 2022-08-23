'''
    PUCPR - Tecnologia em Big Data e Inteligência Analítica - Inverno 2022

    Descrição   : Código fonte standalone para jogo ZombieDice, projeto de Raciocíno Computacional.
    Tutor       : Professor Galbas
    Aluno       : Giovani Drosda Lima | gdrosdalima@gmail.com

'''

# Bibliotecas

from operator import countOf
import time, random, copy

#--

# definição de classes, dicionários e afins [INÍCIO]

class Player:
    def __init__(self, name, description, klass, isBot, hp, brains):
        self.name           = name
        self.description    = description
        self.klass          = klass
        self.isBot          = isBot
        self.hp             = hp
        self.brains         = 0
    #enddef
#endclass

class TotalInGame:
    def __init__(self, qtdplayers, qtdbots):
        self.players = qtdplayers
        self.bots    = qtdbots
        self.total   = self.bots + self.players
    #enddef
#endclass

Klass = {
    0 : {
        'name'          : 'Parrudo',
        'items'         : 0,
        'hp'            : 4,
        'description'   : "Enquanto as outras classes possuem 3 de vida, esta tem 4. Porém, devido ao seu acelerado metabolismo, precisa consumir 15 cérebros para a vitória ao invés de 13."
    },

    1 : {
        'name'          : 'Incansável',
        'items'         : 0,
        'hp'            : 3,
        'description'   : "Caso os 3 dados na rodada deste zumbi resultem em passos, este pode optar por correr mais um pouco e jogar mais um dado para tentar alcançar sua vítima."
    },

    2 : {
        'name'          : 'Ciclista',
        'items'         : 1,
        'hp'            : 3,
        'description'   : "Este zumbi já não anda mais de bicicleta, mas ainda tem um capacete que oferece 50% de chances de protegê-lo do tiro. Durabilidade de 4 tiros."
    },

    3 : {
        'name'          : 'Cowboy',
        'items'         : 1,
        'hp'            : 3,
        'description'   : "Se o cowboy conseguir cérebros na rodada, ele pode optar por trocá-los por laços. Ao jogar um laço, existe 30% de chances de pegar 1 vítima, 15% de pegar 2 e 3% de pegar 3."
    }


    #TODO: add Weeb that gets isekai'd when he dies (1hp)

}


BotNameSyllables = {"kan", "len", "ghi", "flok", "trom", "fle", "dros", "da", "lim", "a", "ki", "ta", "ma", "shi"}

BotGenerationMessages = {
    "Mordendo uns transeuntes...",
    "Selecionando os melhores cérebros...",
    "Fazendo uma pausa pro lanche...",
    "Costurando mandíbulas tortas...",
    "Enchendo linguiça...",
    "Treinando o zumbi...",
    "Enchendo a caneca de café...",
    "Contemplando a paisagem...",
    "Ouvindo grunge...",
    "Motivando o zumbi..."
}

Dices = {
    0: {
        'Cor'       : 'Verde',
        'Passos'    : 2,
        'Tiro'      : 1,
        'Cérebro'   : 3
    },

    1: {
        'Cor'       : 'Amarelo',
        'Passos'    : 2,
        'Tiro'      : 2,
        'Cérebro'   : 2
    },

    2: {
        'Cor'       : 'Vermelho',
        'Passos'    : 2,
        'Tiro'      : 3,
        'Cérebro'   : 1
    }
}

Actions = ['Passos', 'Tiro', 'Cérebro']

PlayersInGame = []

# definição de classes, dicionários e afins [FIM]

def newSection():
    print("\n\n")
    speech("============================================|", .01)
    speech("|######################", .02)
    print("\n\n")
#enddef

def speech(text, speed):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(speed)
        if c == ';' or c == ':' or c == '.':
            time.sleep(1)
        elif c == ',':
            time.sleep(.2)
#enddef

def Welcome():
    speech('ATENÇÃO: este programa usa alguns caracteres UTF-8. Caso seu console não esteja configurado com suporte UTF-8,', .01)
    speech('\n vão aparecer uns bagulhos sinistros na tela.', .01)
    speech('\nAqui uma demonstração desses caracteres: ⣿⣿⣿', .01)
    speech('\nPS: o console do VScode decodifica estes caracteres ^^, o CMD do Windows normalmente não.', .01)
    newSection()
    newSection()
    speech("Olá! Bem vindos ao ZombieDice.\n", .04)
    time.sleep(2)
    speech("Este é um jogo de zumbi, mas antes que você comece a se gabar\n", .01)
    speech("de ser um expert em sobrevivência pós-apocalíptica porque já\n", .01)
    speech("assistiu todas as temporadas de The Walking Dead, fique sabendo que:", .01)
    time.sleep(2)
    speech("\n\n   1. Já pode tirar seu cavalinho da horda de zumbis, Rick Grimes.", .01)
    speech("\n      Neste jogo, VOCÊ É O ZUMBI.", .01)
    time.sleep(1)
    speech("\n\n   2. Para de ser fanboy, aceita logo que TWD fica paia depois da 6 temporada :/", .01)
    time.sleep(3)

    speech("\n\nOk, preparem a pipoca, acomodem-se na cadeira, abram o suco de tamarindo (com sabor de limão)!", .01)
    speech("\nVamos começar. Antes, eu preciso saber quanta gente vai jogar.", .01)
    speech("\nAh, e não se preocupe se tiver pouca gente! Posso usar meus poderes", .01)
    speech("\npsiônicos para invocar uns bots.", .01)

    StartMenu()
#enddef

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

    TotalInThisGame = TotalInGame(quantityOfPlayers, quantityOfBots)

    if TotalInThisGame.total <= 1:
        print("Quer todos os cérebros pra você? ~.o")
        print("Adicione pelo menos 2 jogadores ou bots para iniciar.")
        StartMenu()

    if TotalInThisGame.players == 0:
        print("Robô também sofre, abaixem o preço do i9!")

    
    SetCharacters(TotalInThisGame)
    #ScriptStartGame() TODO descomentar
    StartGame()

#enddef

def SetCharacters(TotalInThisGame):
    if TotalInThisGame.bots > 0:
        newSection()
        GenerateBots(TotalInThisGame.bots)

    if TotalInThisGame.players > 0:
        newSection()
        SetPlayers(TotalInThisGame.players)

#enddef

def GenerateBots(quantityOfBots):
    print("Ok! vou gerar os bots...\n")

    for x in range(random.randint(3, 6)):
        print(random.choice(list(BotGenerationMessages))) #imersão
        time.sleep(1.5)

    print("") #linebreak
    for i in range(quantityOfBots):

        quantityOfSyllables = random.choice([2,3])
        name = ''
        
        for o in range(quantityOfSyllables):
            name += random.choice(tuple(BotNameSyllables))
            
        description = 'bipbop' #TODO add cool descriptions
        klass = random.randint(0, len(Klass) - 1)
        isBot = True

        PlayersInGame.append(Player(name, description, klass, isBot, 3, 0))

        speech("Nasce {}, um zumbi {}!\n".format(name, Klass[klass]['name']), .01)
        time.sleep(.5)

#enddef


def SetPlayers(quantityOfPlayers):
    print("\nJoia. Agora, vamos criar os personagens dos jogadores ^ü^ eba!\n\n")

    for i in range(quantityOfPlayers):
        name = input("Jogador {}, escolha um nome que faça jus à grandeza de seu personagem: ".format(i+1))
        print("\n{}! Que nome digno!\n".format(name))
        time.sleep(3)

        print("Vamos escolher a classe do seu personagem.\n")
        time.sleep(2)
        for x in Klass:
            print("{}. {} - {}".format(x,Klass[x]['name'],Klass[x]['description']))
            time.sleep(1)

        while True:
            try:
                chosenKlass = int(input("\n\nE aí, qual a classe de {}? ".format(name)))
                if chosenKlass in range(0, len(Klass)):
                    break
                else:
                    print('\nOops, parece que a classe não existe. Tente escolher um número entre 0 e {}, correpondente a classe de {}'.format(len(Klass) - 1, name))
            except:
                print('\nOops, parece que a classe não existe. Tente escolher um número entre 0 e {}, correpondente a classe de {}'.format(len(Klass) - 1, name))

        klass = chosenKlass
        speech("Nobre {}!".format(Klass[klass]['name']),.01)
        time.sleep(1)

        print('\nVamos adicionar uma descrição digna para {}.'.format(name))
        description = input('{} é: '.format(name))
        
        isBot = False
        hp = int(Klass[klass]['hp'])
        PlayersInGame.append(Player(name, description, klass, isBot, hp, 0))
        speech('\nUma nova lenda surge: {} ({}), {}\n'.format(name, Klass[klass]['name'], description), .04)

#enddef

def ScriptStartGame():
    speech('\nMestre: A aventura vai começar.\n', .02)
    speech('\nNossos nobres heróis ', .02)
    for h in PlayersInGame:
        speech('{}, {}; '.format(h.name, h.description),.01)
        time.sleep(.4)
    
    speech('partem em sua jornada para salvar o mundo dos zumbis e... ãh?', .02)
    speaker1 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    while speaker1 == speaker2:
        speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name

    speech('\n{}: Que barulho é esse?'.format(speaker1), .02)
    time.sleep(2)
    speech('\n{}: Parece que vem da porta.'.format(speaker2), .02)
    time.sleep(2)
    speech('\n -Frodo, o guarda, vem correndo até a sala. Parece que está com o braço ferido.', .02)
    time.sleep(2)
    speaker1 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    while speaker1 == speaker2:
        speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name

    speech('\nFrodo: Arrgh! {}, {}, pessoal! Emergência!'.format(speaker1, speaker2), .02)
    time.sleep(2)
    speech('\n{}: Frodo! O que houve? Seu braço!'.format(speaker1), .02)
    time.sleep(2)
    speech('\nMestre: Antes que alguém pudesse proferir outras palavras, percebem uma silhueta atrás de Frodo.', .02)
    time.sleep(3)
    print('\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣴⣶⣶⣿⣿⣿⣿⣶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⠈⠉⠀⣿⣿⣿⣿⣿⣷⠀\n⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠃⠀⠀⠀⠀⠀⠀⠀⠀⣿⡟⠹⣿⣿⣿⡆\n⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⡇\n⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⣠⣼⣿⣿⣿⣿⣿⡟⠀⣿⣿⡿⠻⠟⠀⠀⠀⠀⠸⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⣴⣿⣿⣿⣿⣿⣿⣿⣿⡇⢠⣿⣿⡷⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠻⣿⣿⣿⣿⣿⠋⢻⣿⣧⣻⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠙⠛⣿⣿⠏⠀⠀⠉⠃⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡏⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠿⣿⣿⣿⡿')
    speech('zumbi: ', .01)
    time.sleep(3)
    speech('C... Cééééreebrooos...', .05)
    time.sleep(1)
    speech('\n\nMestre: Uma horda de zumbis entra na casa. ', .02)
    time.sleep(2)
    speaker1 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    while speaker1 == speaker2:
        speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name

    speech('{} tenta alcançar o baú onde guardam as armas. Está emperrado. {} tenta ajudá-lo, mas percebe uma pressão sob'.format(speaker1, speaker2),.02)
    speech('\nseu tornozelo. Sua visão fica escura e desmaia.',.02)
    time.sleep(1)

    speech('\n\nMestre: Quando {} acorda, percebe algo diferente: estava verde. Seus amigos também. Frodo havia sumido.'.format(speaker2),.02)
    time.sleep(1)
    speaker1 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    while speaker1 == speaker2:
        speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name

    speech('\n{}: Gente, tem algo errado...'.format(speaker1), .02)
    time.sleep(1)
    speech('\n{}: Uau, Sherlock Holmes, descobriu isso sozinho? Parece que viramos zumbis.'.format(speaker2), .02)
    time.sleep(1)
    speech('\n{}: Paia :/ . Pior que eu to com fome...'.format(speaker1), .02)
    time.sleep(1)

    speaker1 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name
    while speaker1 == speaker2:
        speaker2 = PlayersInGame[random.randrange(0, len(PlayersInGame))].name

    speech('\n{}: Acho que devíamos sair por aí comer uns cérebros, papo reto.'.format(speaker1), .02)
    time.sleep(1)
    speech('\n{}: Devíamos fazer uma competição também, quem enche a barriga primeiro.'.format(speaker2), .02)
    time.sleep(1)
    speech('\n{}: Da hora! Eu tô nessa!'.format(speaker1), .02)
    time.sleep(1)

    speech('\n\nMestre: E então, os mais novos zumbis de Rootenville saíram para buscar vítimas indefesas para\n', .02)
    speech('fins puramente competitivos. ', .02)
    time.sleep(2)
    speech('Que foi, achou que eles teriam que coletar cérebros para salvar o mundo de algum jeito?', .02)

#enddef

def getDice():
    thisDice = (Dices[random.randint(0, len(Dices)-1)])
    print(thisDice)
    return thisDice

#enddef


def StartGame():
    newSection()
    turno = 1
    rodada = 0

    for thisPlayer in PlayersInGame:
        rodada += 1
        if rodada == len(PlayersInGame):
            turno += 1
        speech('Turno {}, rodada de {}!\n'.format(turno, thisPlayer.name), .02)
        speech('\n{}, prepare-se.\n'.format(thisPlayer.name), .02)

        input('Aperte Enter para selecionar seus dados...')

        thisDice = Dices[random.randint(0, len(Dices)-1)]
        speech('\nDado {}!\n'.format(thisDice['Cor']), .02)

        input('Aperte Enter para jogar o dado...')
        speech('\n...\n', .02)
        
        thisAction = random.choices(Actions, weights = (thisDice['Passos'], thisDice['Tiro'], thisDice['Cérebro']), k = 1)

        speech('{}\n'.format(thisAction), .02)

        #TODO tratar dados

#enddef

StartMenu()