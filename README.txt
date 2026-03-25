solvers próprios implementa os três métodos de resolução
integração pysat e solvers próprios define o problema das n rainhas e resolve com o pysat + solvers próprios
teste inicial pysat é a modelagem do problema + resolução pelo pysat.
Com n = 3, método direcional resolve instantâneamente assim como o pysat.
Com n = 4, o mesmo ocorre. 
Com n = 5, método direcional resolve após 40 segundos. 
O método de resolução linear e o ingênuo não resolveram pra n = 3 mesmo depois de 30 minutos mesmo
após tentativas de otimização do código.
A forma geral de modelagem dos três métodos foi por meio do uso de um set de sets imutáveis para guardar as cláusulas iniciais e depois ir adicionando cláusulas novas. Usar set facilita evitar a repetição de cláusulas idênticas. 
Para o método linear, usamos uma estrutura de pilha para guardar os ancestrais que estão no caminho
e testamos para todos os possíveis inicios. 
Para o método de buckets/direcionado, usamos um dicionário para ser cada bucket. 
Como os dois métodos iniciais não foram capazes de resolver o problema das n rainhas, 
acho desnecessário documentar análises sobre tempo, aqui. 