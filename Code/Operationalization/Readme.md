## Esta pasta contém códigos para o deploy do modelo.
- O processo inicia pelo script `process_data.py`, onde realizamos uma varredura no dataset presenta na pasta `Processed/air_pol_delhi.csv`, em seguida realizamos o envio para AWS dos dados.
- Já o segundo script `process_shadow_device.py` realiza a simulação de alteração de estado do nosso Device Shadow utilizado no projeto