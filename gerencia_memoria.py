class Node:
    def __init__(self, tipo, num):
        #livre/ocupado
        self.tipo = tipo
        #numero identificador
        self.num = num
        # inicio e fim do bloco
        self.start = 0
        self.end = 0
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self, max, min):
        nodo = Node('L', 0)
        nodo.start = min
        nodo.end = max
        self.head = nodo
        self.tail = nodo
        #espaco de memoria
        self.max = max
        self.min = min

        self.lista_espera = []


    def add(self,aux, nodo, tamanho):
        if aux.tipo == 'L' and (aux.end - aux.start) > tamanho:

            #primeiro nodo da lista
            if aux == self.head:
                nodo.start = aux.start
                aux.start = aux.start + tamanho
                nodo.end = aux.start
                aux.prev = nodo
                nodo.next = aux
                self.head = nodo
                print("Alocacao Bloco",nodo.num,"entre", nodo.start, "-", nodo.end)
                return True

            # meio da lista
            else:
                nodo.start = aux.start
                aux.start = aux.start + tamanho
                nodo.end = aux.start
                nodo.prev = aux.prev
                aux.prev.next = nodo
                aux.prev = nodo
                nodo.next = aux
                print("Alocacao para o Bloco",nodo.num,"entre",nodo.start,"-",nodo.end)
                return True

        if aux.tipo == 'L' and (aux.end - aux.start) == tamanho:
                aux.num = nodo.num
                aux.tipo = 'S'
                print("Alocacao para o Bloco",aux.num,"entre",aux.start,"-",aux.end)
                return True

        #ultimo nodo da lista
        elif aux == self.tail:
            if not ((nodo,tamanho) in self.lista_espera):
                self.lista_espera.append((nodo,tamanho))
            self.fragmentacao(self.head, tamanho, 0)
            return False
        else:
            return self.add(aux.next, nodo, tamanho)


    #PRINTS / verifica se há fragmentação externa
    def fragmentacao(self, nodo, tamanho, livre):
        if nodo.tipo == "S":
            print(nodo.start, "-", nodo.end, "bloco", nodo.num, "com tamanho igual a:", nodo.end - nodo.start)
        else:
            livre = livre + (nodo.end - nodo.start)
            print(nodo.start, "-", nodo.end, "livre, com tamanho igual a:", nodo.end - nodo.start)
        if nodo == self.tail:
            print(livre," livres,", tamanho, "solicitados - fragmentacao externa")
        else:
            self.fragmentacao(nodo.next, tamanho, livre)


    #libera os blocos após reorganizar
    def liberaBloco(self, nodo,  num):
        if nodo.tipo == 'S' and nodo.num == num:
            nodo.tipo = 'L'
            nodo.num = 0
            start = nodo.start
            end = nodo.end
            print("Bloco",num, "(", start, "-", end, ") liberado")
            self.reorganiza(nodo)
            self.espaco_livre()
        elif nodo == self.tail:
            print("Tamanho inválido.")
        else:
            self.liberaBloco(nodo.next, num)


    #reorganiza os blocos para liberar memória
    def reorganiza(self, nodo):
        if nodo != self.head:
            while nodo.prev.tipo == 'L':
                aux = nodo.prev
                nodo.start = aux.start
                nodo.prev = aux.prev
                if aux == self.head:
                    self.head = nodo
                    break
                aux.prev.next = nodo

        if nodo != self.tail:
            while nodo.next.tipo == 'L':
                aux = nodo.next
                nodo.end = aux.end
                nodo.next = aux.next
                if aux == self.tail:
                    self.tail = nodo
                    break
                aux.next.prev = nodo


    #Procura por espaço na lista para blocos na lista de espera
    def espaco_livre(self):
        bool = False
        for i in range(0,len(self.lista_espera)):
            nodo, tamanho = self.lista_espera[i]
            bool = self.add(self.head, nodo, tamanho)
            if bool:
                #se conseguir adicionar na lista, deleta o mesmo da lista de espera
                del self.lista_espera[i]
                self.espaco_livre()
                break



file =  open('caso2.txt', 'r')
linha = file.readline()
modoUtilizado = int(linha)
linha = file.readline()
mi = int(linha)
linha = file.readline()
mf = int(linha)
listaNodos = LinkedList(mf, mi)

qtdBlocos = 1
for linha in file:
    tipo, num = linha.split(' ')
    num = int(num)
    if tipo == "S":
        nodo = Node(tipo,qtdBlocos)
        listaNodos.add(listaNodos.head, nodo, num)
        qtdBlocos += 1
    elif tipo == "L":
        listaNodos.liberaBloco(listaNodos.head,num)
file.close()