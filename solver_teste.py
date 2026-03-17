#def to_pysat(clausulas):
#    return [list(c) for c in clausulas]

def resolucao(c1, c2):
    resolvente = set()
    
    for l in c1:
        if -l in c2:  # literal complementar 
            new_clause = (c1 - {l}) | (c2 - {-l})
            resolvente.add(frozenset(new_clause)) # adiciona a nova cláusula resolvente, usando frozenset para garantir que seja imutável e possa ser armazenada em um conjunto
    
    return resolvente


def bobinho(clausulas, max_iter=100):
    clausulas = set(map(frozenset, clausulas)) #frozenset é só para trabalharmos com conjuntos de cláusulas.
    #vamos ter um mapa entre as clausulas imutaveis e as clausulas mutaveis, para podermos trabalhar com conjuntos de clausulas e ao mesmo tempo ter a facilidade de manipular as clausulas como listas.
    count = 0
    while True:
        count += 1
        if count > max_iter:
            return "oops"
        new_clausulas = set()
        clause_list = list(clausulas)
        
        # todos os pares
        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                c1 = clause_list[i]
                c2 = clause_list[j]
                
                resolventes = resolucao(c1, c2)
                
                if frozenset() in resolventes:
                    return "UNSAT"
                
                new_clausulas |= resolventes
        
        # se não gerou nada novo
        if new_clausulas.issubset(clausulas):
            return "SAT"
        
        clausulas |= new_clausulas
        #ou seja, vamos aplicando resolução e gerando clausulas novas e adicionando ao conjunto de clausulas, até que ou geramos a clausula vazia (UNSAT) ou não geramos mais nada novo (SAT).