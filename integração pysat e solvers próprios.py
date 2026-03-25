from pysat.solvers import Glucose3
from solver_teste import bobinho, linear, resolucao_direcionada
clausulas = []
n = 5 #n x n do tabuleiro
def mapear(i,j):
    return i*n + j + 1 #pysat nao tem matriz entao temos que pegar a pos especifica no tabuleiro
solver = Glucose3()

#modelando o problema em si:
for i in range(n):
    solver.add_clause([mapear(i,j) for j in range(n)]) #(v_ij v_i(j+1) v_i(j+2) ... v_in) ou seja, pelo menos uma rainha por linha. 
    clausulas.append(set([mapear(i,j) for j in range(n)]))
    for j in range(n):
        for k in range(j+1, n):
            solver.add_clause([-mapear(i,j), -mapear(i,k)]) #(-v_ij v -v_ik) ou seja, no maximo uma rainha por linha 
            clausulas.append(set([-mapear(i,j), -mapear(i,k)]))

#ou seja, fazemos um ou entre as variaveis de cada linha para garantir que haja pelo menos uma rainha por linha, podendo estar em qualquer coluna
#e fazemos um ou entre as negacoes das variaveis de cada linha para garantir que haja no maximo uma rainha.
#a formulação: p_i = (ci1 e ~ci2 e ~ci2 e ~ci3 e ... ~cin) ou (~ci1 e ci2 e ~ci3 e ... ~cin) ou ... (~ci1 e ~ci2 e ~ci3 e ... cin)
#que foi a ideia original que eu tive, não está na CNF, 
#então precisamos converter para CNF, o que é feito pelas cláusulas acima.
#fazemos o mesmo para colunas:
for j in range(n):
    #solver.add_clause([mapear(i, j) for i in range(n)])
    #clausulas.append(set([mapear(i, j) for i in range(n)])) não precisamos garantir isso novaemente
    for i in range(n):
        for k in range(i + 1, n):
            solver.add_clause([-mapear(i, j), -mapear(k, j)])
            clausulas.append(set([-mapear(i, j), -mapear(k, j)]))


#principal, a diferença é a mesma, a maior dif é -n 
for dif in range(-n + 1, n): # para cada diagonal
    diagonais = []
    for i in range(n): # e cada linha
        j = i - dif #calculamos a sua coluna correspondente, já que a dif entre linha e coluna para cada diagonal é constante. 
        if 0 <= j < n:
            diagonais.append(mapear(i, j))
    # e so podemos ter uma rainha por diagonal, entao fazemos um ou entre as negacoes das variaveis de cada diagonal para garantir isso.
    for a in range(len(diagonais)):
        for b in range(a + 1, len(diagonais)):
            solver.add_clause([-diagonais[a], -diagonais[b]])
            clausulas.append(set([-diagonais[a], -diagonais[b]]))
#secundaria, a soma é a mesma, e não a diferença. a maior soma é 2n
for s in range(2*n - 1):
    diag = []
    for i in range(n):
        j = s - i
        if 0 <= j < n:
            diag.append(mapear(i, j))

    for a in range(len(diag)):
        for b in range(a + 1, len(diag)):
            solver.add_clause([-diag[a], -diag[b]])
            clausulas.append(set([-diag[a], -diag[b]]))
#solver
if solver.solve():
    model = solver.get_model()
    for i in range(n):
        for j in range(n):
            if mapear(i, j) in model:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
else:
    print("Sem solução")
clausulas = list(set(map(frozenset, clausulas)))
vars_freq = {}
for c in clausulas:
    for l in c:
        vars_freq[abs(l)] = vars_freq.get(abs(l), 0) + 1

ordem = sorted(vars_freq, key=lambda x: vars_freq[x])
#bobinho(clausulas=clausulas)
#linear(clausulas=clausulas)
print(resolucao_direcionada(clausulas=clausulas, ordem=ordem))
