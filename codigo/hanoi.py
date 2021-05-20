#se tendran 3 torres identificadas
# torre A =  origen /   torre B = destino /      torre c = Auxiliar

#recursividad
def hanoi(Ndiscos, TorreOrigen, TorreDestino, TorreAux):
    if Ndiscos == 1:
        print('pasar disco de {} a {}'.format(TorreOrigen,TorreDestino) )
    else:
        hanoi(Ndiscos-1,TorreOrigen,TorreAux,TorreDestino)
        print('Pasar disco desde {} a {}'.format(TorreOrigen,TorreDestino))
        hanoi(Ndiscos-1,TorreAux,TorreDestino,TorreOrigen)


hanoi(3,'A','C','B')
