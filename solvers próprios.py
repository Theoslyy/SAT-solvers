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
def linear(clausulas):
    clausulas = set(map(frozenset, clausulas))
    visitadas = set(clausulas)
    # estrutura para salvar os ancestrais por meio de um caminho: cada cláusula começa com ela mesma como ancestral
    caminhos = [(c, {c}) for c in clausulas]
    def pode_resolver(c1, c2):
        return any(-l in c2 for l in c1)
    while caminhos: #temos que testar todos os possíveis caminhos iniciais
        atual, ancestors = caminhos.pop()  # pega o próximo caminho a ser explorado
        #nosso espaco de busca e nas clausulas originais e nos ancestrais
        candidatos = clausulas | (ancestors - {atual}) # os candidatos para resolver com a cláusula atual são as cláusulas originais e os ancestrais, exceto a própria cláusula atual
        for c2 in candidatos:
            if not pode_resolver(atual, c2):
                continue
            resolventes = resolucao(atual, c2)

            for r in resolventes:
                if r == frozenset():
                    return "UNSAT"

                if any(lit in r and -lit in r for lit in r):
                    continue

                if r == atual:
                    continue

                if r not in visitadas:
                    visitadas.add(r)
                    novo_anc = ancestors | {r}
                    caminhos.append((r, novo_anc))
    return "SAT"

def resolucao_direcionada(clausulas, ordem):
    clausulas = set(map(frozenset, clausulas))
    
    #cria buckets pra cada variável na ordem dada
    buckets = {v: [] for v in ordem}
    geradas = set(clausulas) #conjunto de clausulas novas geradas, para evitar gerar a mesma clausula mais de uma vez
    #função para achar a variável "mais à esquerda" com precedencia da ordem dada
    def menor_var(clause):
        vars_clause = [abs(l) for l in clause]
        for v in ordem:
            if v in vars_clause:
                return v
        return None

    # preenchendo os buckets com as cláusulas iniciais
    for c in clausulas:
        v = menor_var(c)
        if v is not None:
            buckets[v].append(c)

    # processamento dos buckets
    for v in ordem: # para o bucket da variável v na ordem dada
        bucket = buckets[v]

        pos = [c for c in bucket if v in c] #acha as cláusulas que contém v
        neg = [c for c in bucket if -v in c] #acha as clásulas que contém ¬v

        # resolve cláusulas com v e ¬v
        for c1 in pos:
            for c2 in neg:
                resolventes = resolucao(c1, c2)

                for r in resolventes:
                    if r == frozenset():
                        return "UNSAT"

                    # remove tautologia
                    if any(lit in r and -lit in r for lit in r):
                        continue

                    if r not in geradas:
                        geradas.add(r)
                        novo_v = menor_var(r)
                        if novo_v is not None:
                            buckets[novo_v].append(r)
                        buckets[v] = []

    return "SAT"

#testes abaixo
        
clausulas1 = [
    {1, 2},
    {-1},
    {-2}
]
print(bobinho(clausulas1))
print(linear(clausulas1))
print(resolucao_direcionada(clausulas1, ordem=[1, 2]))
clausulas2 = [
    {1, 2},
    {-1, 3},
    {-2, 3},
    {-3}
]
print(bobinho(clausulas2))  
print(linear(clausulas2))
print(resolucao_direcionada(clausulas2, ordem=[1, 2, 3]))
clausulas3 = [
    {1, 2, 3},
    {-1, 4},
    {-2, 4},
    {-3, 4},
    {-4}
]
print(bobinho(clausulas3))
print(linear(clausulas3))
print(resolucao_direcionada(clausulas3, ordem=[1, 2, 3, 4]))
clausulas4 = [
    {1, 2},
    {-1, 2},
    {1, -2}
]
print(bobinho(clausulas4))
print(linear(clausulas4))
print(resolucao_direcionada(clausulas4, ordem=[1, 2]))
clausulas5 = [
    {1, 2},
    {1, 3},
    {2, 3},
    {-1, -2},
    {-1, -3},
    {-2, -3}
]
print(bobinho(clausulas5))
print(linear(clausulas5))
print(resolucao_direcionada(clausulas5, ordem=[1, 2, 3]))
