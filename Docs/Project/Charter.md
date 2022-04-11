# Descrição do projeto

## Background do negócios

A poluição é um grande problema na maioria das cidades, principalmente na índia onde tem algumas das cidades mais poluídas do mundo. A capital, Nova Delhi, é o coração da índia e também a mais poluída. Essa poluição acaba afetando a saúde e a qualidade de vida das famílias em Delhi.

## Escopo
Este trabalho tem o objetivo de analisar a poluição do ar no período de 5 anos utilizando 5 métricas

## Equipe
* O trabalho foi realizado em grupo de dois alunos do curso de Engenharia da computação do instituto infnet 
  * Rafael Viana Cunha
  * Luis Gomes
	
## Métricas
* O conjunto de dados é composto por cinco sensores: 
  * Anand Vihar,
  * DTU,
  * IGI Airport (T3),
  * Dwarka Setor 8 e
  * North Campus DU.
* A Partir desses sensores vão ser utilizadas as seguintes métricas:
  * PM10
  * PM2.5
  * Ozônio
  * CO
  * SO2
* A timeline dos dados é de janeiro de 2016 até janeiro de 2021.

## Plano
* Analisando os dados inicial crus
* Selecionar apenas dados úteis
* Remover dados duplicados
* Análise exploratória dos dados
* Plotar os dados
* Comparar a relação entre PM2.5 e PM10
* Descobrir quais são os meses tiveram os 15 piores dias
* Os maiores PM2.5 e PM10 por estação
* Entender os níveis de qualidade do ar
* Utilização da ferramenta Facebook Prophet para predizer qual a qualidade do ar nos próximos 3 anos


## Arquitetura
* Dados
  * Os dados estão no formato csv
* Vamos utilizar um notebook em python para analisar o problema 
* AWS IoT para processamento dos dados dos sensores
* Facebook Prophet para predição dos dados

* Diagramas
- Processando dados dos sensores
![processando_dados drawio](https://user-images.githubusercontent.com/7775891/162655291-b796cc21-a4cd-4631-8109-3c0b3ab97598.png)

- Analytics
![analytics drawio](https://user-images.githubusercontent.com/7775891/162655315-d750e5a8-26ca-4ce8-b25b-d569dfbe260f.png)

- Device shadow
![shadow drawio](https://user-images.githubusercontent.com/7775891/162655332-d06409fb-46b8-4be1-a603-77c9159eec5d.png)




