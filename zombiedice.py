'''
    PUCPR - Tecnologia em Big Data e Inteligência Analítica - Inverno 2022

    Descrição   : Código fonte standalone para jogo ZombieDice, projeto de Raciocíno Computacional.
    Tutor       : Professor Galbas
    Aluno       : Giovani Drosda Lima | gdrosdalima@gmail.com

'''

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

# definição de classes, dicionários e afins [FIM]

