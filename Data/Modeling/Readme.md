## Dados dos sensores de qualidade do ar em Delhi

Os valores captados pelos sensores estão sendo enviado para o ambiente da AWS IOT. Dessa forma, para obter o dataset utilizado na modelagem do problema, este será disponibilizado pela ferramenta AWS IOT Analytics.

Para isso, deverá ser acessado o console da AWS Management.
- No console, irá seguir até a ferramente de AWS IOT Analytics
- Em seguinda deverá acessar o dataset `airpollutiondelhidataset`
- Esse dataset contém todos os dados coletados pelos sensores.
- Para realizar o download dos dados, deverá executar a operação de `Run now` para ser gerado uma nova versão do dataset. Depois disso, basta apenas realizar o download dos dados. 
- Renomeie o arquivo para `airpollutiondelhidataset.csv`

Por outro lado, podemos realizar o download dos dados via o link do S3: https://at-luis-gomes.s3.sa-east-1.amazonaws.com/9b00cfb1-9280-4108-9729-7b0f4243deb0.csv