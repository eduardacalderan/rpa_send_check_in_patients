# Envio de check-in para pacientes

***Para o envio de check-in deverá ser pego todos os pacientes que foram atendidos há 30 dias atrás. Esse processo deverá ser feito diariamente. Não pode ser enviado mensagem duplicada para os pacientes no mesmo dia, para isso, todos os contatos são salvos em um excel do dia atual, com o número de telefone, data de envio de mensagem e o status do envio. Através desse excel, é validado se o paciente já recebeu a mensagem ou não. Se ele recebeu, não envia novamente e vai para o próximo. Se ele não recebeu, segue o processo normalmente***.

## Passo a passo do processo realizado

### Passo 1

![Realiza Login na Plataforma](docs/images/first_step.png)
![Imagem de Aguarda Carregamento](docs/images/wait_loading.png)

### Passo 2

![Passa o mouse sobre "Consultório e clica em "Agendamentos"](docs/images/second_step.png)
![Imagem de Aguarda Carregamento](docs/images/wait_loading.png)

### Passo 3

![Clica em "Visão geral"](docs/images/third_step.png)
![Imagem de Aguarda Carregamento](docs/images/wait_loading.png)

### Passo 4

![Clica em "Mês"](docs/images/fourth_step.png)
![Imagem de Aguarda Carregamento](docs/images/wait_loading.png)

### Passo 5

![Passa o mouse sobre o paciente agendado e clica em "confirmar"](docs/images/fifth_step.png)
![Imagem de Aguarda Carregamento](docs/images/wait_loading.png)

### Passo 6

![Com o modal aberto, clica em "solicitar confirmação do paciente"](docs/images/sixth_step.png)

### Passo 7

![Após, clica em "via Whatsapp Web"](docs/images/seventh_step.png)

### Passo 8

![Seleciona "Check-in" como o modelo de mensagem](docs/images/eighth_step.png)

### Passo 9

![Clica no botão de confirmação"](docs/images/ninth_step.png)

### Passo 10

Nessa etapa é realizada a validação para saber se o número de telefone já foi processado ou não. Para isso, é lido um excel do dia atual, com o número de telefone, data de envio de mensagem e o status do envio. Através desse excel, é validado se o paciente já recebeu a mensagem ou não. Se ele recebeu, não envia novamente e vai para o próximo. Se ele não recebeu, segue o processo normalmente  
![Sendo direcionado para a página do WhatsApp, clica em "Iniciar conversa"](docs/images/tenth_step.png)

### Passo 11

![Clica em "Usar o WhatsApp Web"](docs/images/eleventh_step.png)

### Passo 12

![Clica no ícone de envio](docs/images/twelfth_step.png)
