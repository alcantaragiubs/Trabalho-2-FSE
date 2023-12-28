# Trabalho 2 (2023-2)

Trabalho 2 da disciplina de Fundamentos de Sistemas Embarcados - Controle de um Elevador

## Visão Geral

O trabalho envolve o desenvolvimento do software que efetua o controle completo de um elevador incluindo o controle de movimentação, acionamento dos botões internos e externos e monitoramento de temperatura. O movimento do elevador é controlado à partir de um motor elétrico e a posição é sinalizada à partir de sensores de posição e um encoder.
O controle do elevador deve responder aos comandos dos usuários pelo botões externos (andares) ou internos (painel de botões do elevador).

![image](https://github.com/FSE-2023-2/trabalho-2-2023-2-alcantaragiubs/assets/54143767/1fde9567-7076-4ced-bf4a-7617e57e0baa)

![image](https://github.com/FSE-2023-2/trabalho-2-2023-2-alcantaragiubs/assets/54143767/58afab15-4521-4f5a-9b43-669ebdf7e8d5)

![image](https://github.com/FSE-2023-2/trabalho-2-2023-2-alcantaragiubs/assets/54143767/11187791-b9ef-41d9-9023-54c97ca5f9b7)


## Apresentação

  | Conteúdo | Vídeo                                                                                         |
  | -------- | --------------------------------------------------------------------------------------------- |
  | Trabalho 2 | [URL do Vídeo]()  

## Execução do Projeto

### Pré-Requisitos

- SSH
- Estar num terminal linux (ou WSL dele para Windows)

### Execução do Projeto

#### Clone o repositório

```bash 
$ git clone https://github.com/alcantaragiubs/Trabalho-2-FSE.git
```

#### Abra um terminal e entre no ssh da placa 7
```bash 
$ ssh seu-usuario@164.41.98.29 -p 13508
```

- obs: como no projeto  está configurado para a placa rasp47, é indicado utiliza-la para rodar o projeto, caso se deseje acessar outra placa.

#### Entre no caminho da pasta para enviar 

```bash
$ cd .\Trabalho-2-FSE
```

#### Entre no caminho da pasta para enviar 

```bash
$ cd .\Trabalho-2-FSE
```

#### Envie a pasta de elevadores

```bash 
$ scp -P 13508 -r ./elevadores seu-usuario@164.41.98.29:~/
```

#### Entre no terminal da cada placa 
```bash 
$ cd ./elevadores
```

#### Execute os arquivos do

```bash 
$ python controle.py
```

## Utilização do projeto
Para utilização do projeo acesse o [dashboard](http://thingsboard.lappis.rocks:443/dashboard/dd966c20-7a71-11ee-8912-256947be8337?publicId=ba042a80-0322-11ed-9f25-414fbaf2b065) da placa referida (obs: caso mude a placa da configuração padrão, acesse o dashboard referente a ela)
