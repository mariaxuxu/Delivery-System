# Pizzaria dos Henrique's Benitez (Sistema de Delivery CLI)

##### Maria Clara Redin Benitez, 23013156 | Paulo Henrique Correa - 23016227

Este projeto é um sistema de pedidos de delivery desenvolvido em Python que roda via Linha de Comando (CLI).

O objetivo principal da aplicação é demonstrar a implementação prática de 6 Padrões de Projeto (Design Patterns) do GoF 
em um cenário real de engenharia de software, simulando o fluxo de um aplicativo como o iFood.

## Funcionalidades
- **Menu Interativo:** Interface amigável via terminal para realizar pedidos.

- **Catálogo de Produtos:** Visualização de itens disponíveis (Pizzas, Bebidas, Lanches).

- **Personalização (Decorators):** Adição de extras (Bacon, Embalagem de Presente) dinamicamente.

- **Cálculo de Frete (Strategy):** Regras de preço diferentes para Motoboy, Drone ou Clientes VIP.

- **Fluxo de Status (State):** Controle de transição rigoroso (Criado -> Cozinha -> Rota -> Entregue).

- **Notificações (Observer):** Disparo de alertas simulados (E-mail e App do Restaurante) a cada mudança de status.

- **Persistência (Singleton):** Salvamento automático do histórico de pedidos em arquivo JSON.

## Arquitetura e Padrões de Projeto
Abaixo, a lista dos padrões implementados e onde encontrá-los na estrutura do código:

| Padrão | Categoria | Arquivo Local | Descrição da Aplicação |
| :--- | :--- | :--- | :--- |
| **Singleton** | Criacional | `src/database.py` | Garante uma instância única para o gerenciamento e escrita no arquivo de banco de dados (`database.json`). |
| **Builder** | Criacional | `src/builders.py` | Facilita a criação do objeto complexo `Order`, permitindo a adição passo-a-passo de produtos e configurações. |
| **Strategy** | Comportamental | `src/strategies.py` | Define algoritmos intercambiáveis de cálculo de frete e descontos (Moto, Drone, VIP). |
| **State** | Comportamental | `src/states.py` | Gerencia o ciclo de vida do pedido, impedindo transições inválidas (ex: entregar pedido não pago). |
| **Observer** | Comportamental | `src/observers.py` | Notifica automaticamente o Cliente (Email) e o Restaurante sempre que o status do pedido muda. |
| **Decorator** | Estrutural | `src/decorators.py` | Permite adicionar funcionalidades extras (Bacon, Embalagem) aos produtos em tempo de execução sem criar subclasses. |

## Estrutura de Arquivos

```text
ifood_system/
│
├── data/                  # Diretório gerado automaticamente para persistência
│   └── database.json      # Histórico de pedidos salvos
│
├── src/                   # Código Fonte (Core)
│   ├── models.py          # Classes de dados (Cliente, Produto)
│   ├── menu.py            # Catálogo de produtos estático
│   ├── database.py        # Implementação do Singleton
│   ├── builders.py        # Implementação do Builder
│   ├── strategies.py      # Implementação do Strategy
│   ├── states.py          # Implementação do State
│   ├── observers.py       # Implementação do Observer
│   └── decorators.py      # Implementação do Decorator
│
├── tests/                 # Testes Automatizados
│   └── test_core.py       # Testes unitários cobrindo os 6 padrões
│
└── main.py                # Arquivo Principal (Executável)           
```

## Instruções de Execução
### Pré-requisitos
- Python 3.8 ou superior instalado.
- Não é necessário instalar bibliotecas externas (o projeto utiliza apenas bibliotecas padrão do Python).

#### Executar a Aplicação (Modo Interativo) 
Dentro da pasta ifood_system 
```
python main.py
```
Siga as instruções na tela para digitar seu nome, escolher produtos do menu e finalizar o pedido.

#### Executar os Testes Automatizados
Dentro da pasta ifood_system
```
python -m unittest discover tests
```