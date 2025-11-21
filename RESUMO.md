## Relatório Técnico: Implementação de Padrões de Projeto em Sistema de Delivery

- Atividade: Desenvolvimento de Sistema com Padrões de Projeto
- Contexto: Sistema CLI de Delivery (iFood Simplificado) 
- Autores: Maria Clara Redin Benitez - 23013156 | Paulo Henrique Correa - 23016227

## 1. Introdução
   Este documento descreve a arquitetura de software utilizada no desenvolvimento de um sistema de pedidos de delivery 
via linha de comando. O objetivo principal foi a aplicação prática de seis padrões de projeto para resolver 
problemas comuns de desenvolvimento, como acoplamento rígido, complexidade de algoritmos e gerenciamento de estados.

## 2. Descrição dos Padrões Estudados

### 2.1. Singleton (Criacional)
- **Propósito:** Garantir que uma classe tenha apenas uma única instância e fornecer um ponto global de acesso a ela.
- **Estrutura:** Uma classe que contém uma instância estática privada de si mesma e um método estático público para recuperar essa instância.
- **Quando utilizar:** Quando é necessário controlar o acesso a algum recurso compartilhado (como um arquivo ou conexão de banco de dados).

### 2.2. Builder (Criacional)
- **Propósito:** Separar a construção de um objeto complexo da sua representação, permitindo que o mesmo processo de construção crie representações diferentes.
- **Estrutura:** Um "Diretor" ou o próprio cliente chama métodos de um "Builder" passo a passo, e o Builder retorna o produto final.
- **Quando utilizar:** Para evitar construtores com muitos parâmetros e quando o objeto precisa ser montado em etapas.

### 2.3. Strategy (Comportamental)
- **Propósito:** Definir uma família de algoritmos, encapsular cada um deles e torná-los intercambiáveis.
- **Estrutura:** Uma interface comum implementada por várias classes concretas. O contexto possui uma referência para a interface.
- **Quando utilizar:** Quando existem várias formas de executar uma operação (ex: cálculo do frete) e se deseja trocar essa lógica em tempo de execução.

### 2.4. State (Comportamental)
- **Propósito:** Permitir que um objeto altere seu comportamento quando seu estado interno muda. O objeto parecerá ter mudado de classe.
- **Estrutura:** O contexto delega as chamadas de métodos para um objeto de estado atual.
- **Quando utilizar:** Quando o comportamento de um objeto depende do seu estado e ele deve mudar de comportamento em tempo de execução dependendo desse estado (ex: pedido pago vs. pedido enviado).

### 2.5. Observer (Comportamental)
- **Propósito:** Definir uma dependência um-para-muitos entre objetos, de modo que quando um objeto muda de estado, todos os seus dependentes são notificados automaticamente.
- **Estrutura:** Um "sujeito" mantém uma lista de "observadores" e notifica-os chamando seus métodos de atualização.
- **Quando utilizar:** Para implementar sistemas de eventos ou notificações desacopladas.

### 2.6. Decorator (Estrutural)
- **Propósito:** Adicionar responsabilidades a um objeto dinamicamente. Fornece uma alternativa flexível à suboclasse para estender a funcionalidade.
- **Estrutura:** O Decorator envolve o objeto original, implementando a mesma interface, e adiciona comportamento antes ou depois de delegar a chamada.
- **Quando utilizar:** Para adicionar funcionalidades (como "bacon extra") sem criar uma explosão de subclasses.

## 3. Iterações e Variações

### 3.1. Singleton (Database)
- **Implementação no Projeto:** Utilizamos o método mágico __new__ do Python. A instância não é criada na importação do módulo, 
mas apenas na primeira chamada Database(). Isso economiza memória se o banco nunca for acessado.
- **Variação - Módulo Python:** Em Python, módulos são Singletons por natureza. Poderíamos ter criado um arquivo db_module.py 
com variáveis globais, mas optamos pela classe para permitir extensibilidade futura e métodos de instância.
- **Variação - Thread-Safe:** Em ambientes multithread, esta implementação precisaria de um mecanismo de 
bloqueio dentro do __new__ para evitar que duas threads criem instâncias simultâneas.

### 3.2. Builder (OrderBuilder)
- **Implementação no Projeto:** O Builder retorna a própria instância (return self) em métodos como add_product 
e with_extra_bacon. Isso permite o encadeamento de chamadas (builder.add().with().build()), criando uma DSL interna.
- **Implementação no Projeto:** Optamos por não ter uma classe Director separada. O código cliente (main.py e menu.py)
atua como o Diretor, decidindo quais passos executar.
- **Variação - Inner Class:** Em linguagens como Java, é comum o Builder ser uma classe estática interna da classe Produto
(Order.Builder). Em Python, classes separadas são preferidas para manter a clareza.

### 3.3. Strategy (DeliveryStrategy)
- **Implementação no Projeto (Classes Abstratas):** Usamos herança de uma classe base abstrata. Isso garante que todas as 
estratégias tenham estritamente a mesma assinatura de método (calculate_total).
- **Variação - Estratégia Funcional (Lambdas):** Como Python trata funções como objetos de primeira classe, poderíamos ter 
eliminado as classes MotoDelivery/DroneDelivery e passado apenas funções simples como argumento para o Pedido. 
Optamos por classes para permitir que as estratégias tenham estado próprio ou métodos auxiliares no futuro.

### 3.4. State (OrderState)
- **Implementação no Projeto:** Adotamos a abordagem onde o próprio Estado Concreto decide qual é o próximo estado 
(ex: CookingState sabe que o próximo é OnRouteState).
- **Variação - Contexto Gerencia Transição:** Outra forma seria o Contexto (Order) ter as regras de transição 
(if current is Cooking, next is OnRoute). Nossa escolha descentralizada reduz a complexidade ciclomática do Contexto.
- **Variação - State como Singleton:** Como nossos objetos de estado não guardam dados locais (são stateless), poderíamos 
ter feito cada Estado ser um Singleton para economizar memória, em vez de instanciar new CookingState() a cada transição.

### 3.5. Observer (OrderObserver)
- **Implementação no Projeto:** O sujeito (Order) envia os dados necessários (id e status) como argumentos no método update(). 
Os observadores recebem a informação passivamente.
- **Variação - Modelo Pull:** O sujeito poderia enviar apenas uma notificação vazia ("algo mudou"). O observador então teria 
que chamar um método do Sujeito (ex: order.get_status()) para descobrir o que mudou. O modelo Push foi escolhido para reduzir o tráfego de chamadas.
- **Variação - Event Bus:** Poderíamos usar um intermediário global em vez de registrar observadores diretamente no objeto pedido, 
desacoplando ainda mais os componentes.

### 3.6. Decorator (ProductDecorator)
- **Implementação no Projeto:** Usamos composição. O decorator "tem um" produto dentro dele e implementa a mesma interface. 
Isso permite decorar um objeto que já foi decorado (bacon sobre queijo sobre burger).
- **Variação:** Python tem uma sintaxe de decoradores de função/classe (@wrapper). Não utilizamos isso aqui porque os 
Python Decorators são aplicados em tempo de definição de classe, enquanto nosso padrão Decorator precisa adicionar comportamento 
(bacon/embalagem) em tempo de execução.

## 4. Comparações

### 4.1. Strategy vs. State
- **Semelhança:** Estruturalmente, são idênticos em UML. Ambos baseiam-se em composição: o objeto principal delega o trabalho 
para um objeto "ajudante".
- **Diferença:** A intenção. No Strategy (DeliveryStrategy), o cliente escolhe a estratégia uma vez (moto ou drone) e ela 
raramente muda durante a vida do objeto. No State (OrderState), a troca de comportamento é dinâmica, frequente e, muitas 
vezes, automática, sem intervenção do cliente externo.

### 4.2. Builder vs. Factory Method
- **Semelhança:** Ambos são padrões Criacionais focados em abstrair a lógica de instanciação (new).
- **Diferença:** O Factory Method cria o objeto de uma só vez. O Builder constrói o objeto passo a passo. No projeto, 
usamos Builder porque um pedido varia muito em composição, enquanto um Factory seria limitado a tipos pré-definidos.

### 4.3. Decorator vs. Adapter
- **Semelhança:** Ambos "envolvem" um objeto existente.
- **Diferença:** O Adapter muda a interface do objeto para ele se encaixar em outro sistema. O Decorator mantém a interface 
original, mas adiciona novas funcionalidades ou dados (como somar o preço do bacon ao preço original).

### 4.4. Observer vs. Chain of Responsibility
- **Combinação Possível:** Poderíamos usar Chain of Responsibility para tratar o pedido (ex: Validação -> Pagamento -> Cozinha).
- **Diferença:** No Chain, a requisição passa de um para um até ser tratada. No Observer (nosso caso), o evento é disparado 
para todos os interessados simultaneamente. Escolhemos Observer porque tanto o Log quanto o Email precisam saber da mudança ao mesmo tempo.

### 4.5. Integração Builder + Strategy + Observer
- **Sinergia no Projeto:** O código demonstra uma poderosa combinação: O Builder é utilizado para orquestrar a injeção das 
dependências dos outros padrões. É dentro do Builder que decidimos qual Strategy (Moto/Vip) usar e onde registramos os 
Observers. Isso centraliza a complexidade de configuração, deixando a classe Order limpa para focar apenas na lógica de negócio (via State).

## 5. Justificativa Detalhada das Escolhas
   
### 5.1. Padrão Singleton (src/database.py)
- **Por que foi escolhido:** O sistema precisa manipular um único arquivo JSON (database.json).
- **Problema que resolve:** Evita conflitos de concorrência onde múltiplas instâncias tentariam abrir e escrever no arquivo 
simultaneamente, o que poderia corromper os dados.
- **Benefícios:** Centralização do acesso aos dados e controle de estado global do log.
- **Sem o padrão:** Teríamos que passar a referência do arquivo de banco de dados para todas as classes 
(Pedido, Builder, Cliente), gerando alto acoplamento e poluição de código.

### 5.2. Padrão Builder (src/builders.py)
- **Por que foi escolhido:** A criação de um Order envolve muitos passos: associar cliente, definir estratégia, 
adicionar lista de produtos, configurar observadores e estado inicial.
- **Problema que resolve:** Elimina o "Anti-padrão do Construtor Telescópio" (ex: new Order(cliente, null, null, true, false...)).
- **Benefícios:** Torna o código do cliente (no main.py) extremamente legível e permite a construção passo-a-passo interativa.
- **Sem o padrão:** O código no menu interativo seria complexo e difícil de manter, exigindo a criação de todos os 
objetos auxiliares antes de instanciar o pedido.

### 5.3. Padrão Strategy (src/strategies.py)
- **Por que foi escolhido:** O cálculo do valor total varia dependendo de regras de negócio voláteis (Moto, Drone, Cliente VIP).
- **Problema que resolve:** Elimina grandes blocos condicionais (if type == 'MOTO' ... elif type == 'VIP' ...) dentro da classe Order.
- **Benefícios:** Segue o princípio Open/Closed. Podemos adicionar uma nova forma de entrega ("Carro Autônomo") 
criando apenas um novo arquivo, sem tocar na classe Order.
- **Sem o padrão:** A classe Order cresceria indefinidamente a cada nova regra de negócio, tornando-se difícil de testar e manter.

### 5.4. Padrão State (src/states.py)
- **Por que foi escolhido:** Um pedido tem regras estritas de transição. Não se pode cancelar um pedido que já saiu para 
entrega, nem entregar um pedido que não foi pago.
- **Problema que resolve:** Remove a complexidade de flags booleanas (isPaid, isDelivered, isCooking) e condicionais aninhadas.
- **Benefícios:** Encapsula a lógica de transição. Cada estado sabe qual é o próximo. Garante a integridade do fluxo de negócio.
- **Sem o padrão:** O método advance() do pedido seria um monstro cheio de if/else, propenso a bugs lógicos onde um pedido 
poderia pular etapas indevidamente.

### 5.5. Padrão Observer (src/observers.py)
- **Por que foi escolhido:** O sistema precisa realizar ações colaterais (enviar e-mail, logar, avisar cozinha) quando o 
status muda.
- **Problema que resolve:** Acoplamento. A classe Order não deve saber como enviar e-mail ou como funciona a API do restaurante.
- **Benefícios:** Desacoplamento total. Podemos adicionar novos notificadores (ex: SMS, Push Notification) sem alterar 
uma linha de código da classe Order.
- **Sem o padrão:** A classe Order teria dependências diretas de bibliotecas de e-mail e log, violando o Princípio da 
Responsabilidade Única.

### 5.6. Padrão Decorator (src/decorators.py)
- **Por que foi escolhido:** Os produtos podem ter adicionais opcionais (Bacon, Embalagem) que alteram preço e descrição.
- **Problema que resolve:** Explosão de subclasses. Sem ele, teríamos que criar: HamburguerComBacon, HamburguerComEmbalagem,
HamburguerComBaconEEmbalagem.
- **Benefícios:** Flexibilidade. Podemos combinar adicionais infinitamente em tempo de execução.
- **Sem o padrão:** O sistema de cardápio seria rígido e impossível de escalar com novas opções de adicionais.