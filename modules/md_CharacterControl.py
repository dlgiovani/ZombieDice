'''
    PUCPR - Tecnologia em Big Data e Inteligência Analítica - Inverno 2022

    Descrição   : Módulo de controle de personagens para jogo ZombieDice, projeto de Raciocíno Computacional.
    Tutor       : Professor Galbas
    Aluno       : Giovani Drosda Lima | gdrosdalima@gmail.com

'''

import modules.md_UiFunctions as UI
import random, time, copy


Dices = {
    0: {
        'Cor'       : 'Verde',
        'Passos'    : 2,
        'Tiro'      : 1,
        'Cérebro'   : 3,
        'Quantidade': 6
    },

    1: {
        'Cor'       : 'Amarelo',
        'Passos'    : 2,
        'Tiro'      : 2,
        'Cérebro'   : 2,
        'Quantidade': 4
    },

    2: {
        'Cor'       : 'Vermelho',
        'Passos'    : 2,
        'Tiro'      : 3,
        'Cérebro'   : 1,
        'Quantidade': 3
    }
}

DicesIndexes = []
for i in Dices:
    DicesIndexes.append(i)

Actions = ['Passos', 'Tiro', 'Cérebro']


PlayersInGame = []

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


class Player:
    def __init__(self, name, description, klass, isBot, hp, brains):
        self.name           = name
        self.description    = description
        self.klass          = klass
        self.isBot          = isBot
        self.hp             = hp
        self.brains         = 0
    #enddef

    def getPlayer(name, description, klass, isBot, hp, brains):
        return {'name': name, 'description': description, 'klass': klass, 'isBot': isBot, 'hp': hp, 'brains': brains}
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
        'fullBelly'     : 15,
        'description'   : "Enquanto as outras classes possuem 3 de vida, esta tem 4. Porém, devido ao seu acelerado metabolismo, precisa consumir 15 cérebros para a vitória ao invés de 13."
    },

    1 : {
        'name'          : 'Normal',
        'items'         : 0,
        'hp'            : 3,
        'fullBelly'     : 13,
        'description'   : "3 de vida, 13 cérebros pra encher o bucho. Nada de mais. Um zumbi normal."
    },

    #TODO: ↓
    # 2 : {
    #     'name'          : 'Incansável',
    #     'items'         : 0,
    #     'hp'            : 3,
    #     'fullBelly'     : 13,
    #     'description'   : "Caso os 3 dados na rodada deste zumbi resultem em passos, este pode optar por correr mais um pouco e jogar mais um dado para tentar alcançar sua vítima."
    # },

    # 3 : {
    #     'name'          : 'Ciclista',
    #     'items'         : 1,
    #     'hp'            : 3,
    #     'fullBelly'     : 13,
    #     'description'   : "Este zumbi já não anda mais de bicicleta, mas ainda tem um capacete que oferece 50% de chances de protegê-lo do tiro. Durabilidade de 4 tiros."
    # },

    # 4 : {
    #     'name'          : 'Cowboy',
    #     'items'         : 1,
    #     'hp'            : 3,
    #     'fullBelly'     : 13,
    #     'description'   : "Se o cowboy conseguir cérebros na rodada, ele pode optar por trocá-los por laços. Ao jogar um laço, existe 30% de chances de pegar 1 vítima, 15% de pegar 2 e 3% de pegar 3."
    # }


    #TODO: add Weeb that gets isekai'd when he dies (1hp)

}


'''

SetCharacters: chama funções para criar personagens, bots e humanos

'''

def SetCharacters(TotalInThisGame):
    PlayersInGame = []
    if TotalInThisGame.bots > 0:
        UI.newSection()
        PlayersInGame += (GenerateBots(TotalInThisGame.bots))

    if TotalInThisGame.players > 0:
        UI.newSection()
        PlayersInGame += (SetPlayers(TotalInThisGame.players))

    return PlayersInGame

#enddef

'''

GenerateBots: gera bots, seus nomes e classes, e os adiciona na lista de jogadores

'''

def GenerateBots(quantityOfBots):
    print("Ok! vou gerar os bots...\n")
    ThisBotsInGame = []
    for x in range(random.randint(3, 6)):
        print(random.choice(list(BotGenerationMessages))) #imersão
        time.sleep(1.2)

    print("") #linebreak
    for i in range(quantityOfBots):
        quantityOfSyllables = random.choice([2,3])
        name = ''
        
        for o in range(quantityOfSyllables):
            name += random.choice(tuple(BotNameSyllables))
            
        description = 'bipbop' #TODO add cool descriptions
        klass = random.randint(0, len(Klass) - 1)
        isBot = True

        ThisBotsInGame.append(Player.getPlayer(name, description, klass, isBot, 3, 0))

        UI.speech("Nasce {}, um zumbi {}!\n".format(name, Klass[klass]['name']), .01)
        time.sleep(.5)

    return ThisBotsInGame

#enddef

'''

SetPlayers: Define jogadores humanos a partir de inputs do usuário, e os adiciona a lista de jogadores.

'''

def SetPlayers(quantityOfPlayers):
    print("\nJoia. Agora, vamos criar os personagens dos jogadores ^ü^ eba!\n\n")
    ThisPlayersInGame = []
    for i in range(quantityOfPlayers):
        name = ''
        while name.strip() == '':
            name = input("Jogador {}, escolha um nome que faça jus à grandeza de seu personagem: ".format(i+1))
        
        name = name.strip()
        print("\n{}! Que nome digno!\n".format(name))
        time.sleep(3)

        print("Vamos escolher a classe do seu personagem.\n")
        print('(Classes listadas já estão funcionando :D\nno futuro, serão adicionadas mais classes. Já é possível dar um sneak peek no código...)\n')
        time.sleep(2)
        for x in Klass:
            print("{}. {}   - {}".format(x,Klass[x]['name'],Klass[x]['description']))
            time.sleep(.03)

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
        UI.speech("Nobre {}!".format(Klass[klass]['name']),.01)
        time.sleep(1)

        print('\nVamos adicionar uma descrição digna para {}.'.format(name))
        description = input('{} é: '.format(name))
        
        isBot = False
        hp = int(Klass[klass]['hp'])
        ThisPlayersInGame.append(Player.getPlayer(name, description, klass, isBot, hp, 0))
        UI.speech('\nUma nova lenda surge: {} ({}), {}\n'.format(name, Klass[klass]['name'], description), .04)

    return ThisPlayersInGame

#enddef


'''

'''
def play(PlayersInGame):
    for currentPlayer in PlayersInGame: # Para cada jogador listado
        steps       = 0
        shots       = 0
        brains      = 0
        dices       = 0
        shotDices   = {'Verde': 0, 'Amarelo': 0, 'Vermelho': 0} #TODO: load from dict
        playerIsPlaying = True
        UI.speech('\nTurno de {}!\nNo momento, tem {} cérebros.'.format(currentPlayer['name'], currentPlayer['brains']), .03)
        UI.speech('\n{}, prepare-se.\n'.format(currentPlayer['name']), .03)

        DiceTube = copy.deepcopy(Dices) #tubo a ser utilizado no turno do próximo jogador, resetado para o default sempre que muda de jogador
        DiceTube[0]['Quantidade']   = Dices[0]['Quantidade']
        DiceTube[1]['Quantidade']   = Dices[1]['Quantidade']
        DiceTube[2]['Quantidade']   = Dices[2]['Quantidade']

        while playerIsPlaying: #este boolean será falso quando o jogador não quiser pegar mais 3 dados ou quando receber 3 tiros no turno.
            if not currentPlayer['isBot']:
                input('Aperte Enter para selecionar seus dados...')
            dices += 1

            #escolhendo o dado no tubo
            thisDice = DiceTube[random.choices(DicesIndexes, weights = [DiceTube[0]['Quantidade'], DiceTube[1]['Quantidade'], DiceTube[2]['Quantidade']], k = 1)[0]]
            thisDice['Quantidade'] -= 1
            #print('dados no tubo \n{}'.format(DiceTube)) #TODO quando chegar em 13, dados que não resultaram em tiros devem voltar ao tubo.
            UI.speech('\nDado {}!\n'.format(thisDice['Cor']), .03)

            if not currentPlayer['isBot']:
                input('Aperte Enter para jogar o dado...')
            UI.speech('\n•••\n', .03)
            
            #escolhendo a face no dado
            thisAction = random.choices(Actions, weights = (thisDice['Passos'], thisDice['Tiro'], thisDice['Cérebro']), k = 1)

            match thisAction[0]:
                case 'Passos':
                    steps += 1
                case 'Tiro':
                    shots += 1
                    shotDices[thisDice['Cor']] += 1
                case 'Cérebro':
                    brains += 1

            UI.speech('-> {}!\nTotais neste turno:\n'.format(thisAction[0]), .01)
            print(' - Passos: {}\n - Tiros: {}\n - Cérebros: {}\n'.format(steps, shots, brains))

            if shots >= currentPlayer['hp']:
                UI.speech('\nOh não, você perdeu este turno!\n', .03)
                playerIsPlaying = False
                break

            if dices >= 3:
                print('---\nDados restantes no tubo:')
                for leftDice in DiceTube:
                    print(f"{DiceTube[leftDice]['Cor']}: {DiceTube[leftDice]['Quantidade']}")

                while True:
                    UI.speech('---\nDeseja pegar mais 3 dados para jogar? (S/N)\n', .03)
                    if not currentPlayer['isBot']:
                        try:
                            keepPlaying = str.lower(input())
                        except:
                            UI.speech('\nOops, digite S para sim ou N para não.\n', .03)
                    else:
                        keepPlaying = 'n' #bot medroso pra acelerar a gameplay, TODO: keepPlaying <- prob('s' = ?, 'n' = ?)
                    
                    if keepPlaying in ('s', 'n'):
                        break
                    else:
                        UI.speech('\nOops, digite S para sim ou N para não.\n', .03)
            
                if keepPlaying == 's':
                    dices = 0
                    totalInTube = 0
                    for q in DiceTube:
                        totalInTube += DiceTube[q]['Quantidade']
                    if totalInTube < 3:
                        UI.speech('\nRedefinindo dados no tubo, exceto aqueles que resultaram em tiros...\n', .03)
                        DiceTube = copy.deepcopy(Dices) #tubo a ser utilizado no turno do próximo jogador, resetado para o default sempre que muda de jogador
                        DiceTube[0]['Quantidade']   = Dices[0]['Quantidade'] - shotDices['Verde']
                        DiceTube[1]['Quantidade']   = Dices[1]['Quantidade'] - shotDices['Amarelo']
                        DiceTube[2]['Quantidade']   = Dices[2]['Quantidade'] - shotDices['Vermelho']
                        for leftDice in DiceTube:
                            print(f"{DiceTube[leftDice]['Cor']}: {DiceTube[leftDice]['Quantidade']}")

                else: #keepPlaying == 'n'
                    currentPlayer['brains'] += brains
                    playerIsPlaying = False
                    UI.speech('{} termina seu turno com\n - {} Cérebros\n - Sofrendo {} Tiros, avançando com {} cérebros no total.'.format(currentPlayer['name'], brains, shots, currentPlayer['brains']), .03)
                    break

        UI.newSection()
        UI.speech('\nA rodada terminou. Estatísticas:\n', .04)
        for p in PlayersInGame:
            print('\n{}: {} cérebros'.format(p['name'], p['brains']))
#enddef

'''

'''
def tiebreak(PlayersInGame):
    maxBrains = 0
    tieList = []
    for thisPlayer in PlayersInGame:
        if thisPlayer['brains'] == Klass[thisPlayer['klass']]['fullBelly']:
            tieList.append(thisPlayer)

    if len(tieList) > 1:
        UI.newSection()
        UI.speech('**\nTemos dois vencedores na rodada. Hora do desempate! Quem conseguir mais cérebros no desempate, ganha!\n**', .03)
        time.sleep(1)
        foundWinner = False
    else:
        return tieList[0]['name']
    
    while not foundWinner:
        play(tieList)

        for thisPlayer in tieList:
            thisPlayerGain = thisPlayer['brains'] - Klass[thisPlayer['klass']]['fullBelly']
            if thisPlayerGain > maxBrains:
                maxBrains = thisPlayerGain

        listOfTopTie = []
        for thisPlayer in tieList:
            if thisPlayer['brains'] - Klass[thisPlayer['klass']]['fullBelly'] == maxBrains:
                listOfTopTie.append(thisPlayer)
        
        tieList = []
        tieList = listOfTopTie
        if len(listOfTopTie) == 1:
            foundWinner = True

    return listOfTopTie[0]['name']

#enddef

'''

'''

def congratulateWinner(champion):
    UI.newSection()
    UI.speech('- - - - - Temos um vencedor! - - - - -\n', .07)
    time.sleep(1)
    UI.speech('\n**************************************', .03)
    print(f'\n- - - - - Parabéns {champion}! - - - - -')
    UI.speech('**************************************', .03)
    UI.newSection()