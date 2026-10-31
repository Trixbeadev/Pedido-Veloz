# Roteiro passo a passo do vídeo (até 4 minutos)

Este roteiro foi escrito para ser seguido durante a gravação. O texto entre aspas é uma sugestão do que falar. Os itens **Na tela** dizem o que abrir ou executar.

## Antes de gravar

1. Abra o Docker Desktop e espere ele indicar que está funcionando.
2. Abra o projeto `Pedidos-Veloz` no VS Code. Abra um terminal PowerShell na pasta do projeto.
3. Se ainda não existir o arquivo `.env`, crie-o a partir do exemplo:

   ```powershell
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   ```

4. Inicie a aplicação e espere os serviços ficarem prontos:

   ```powershell
   docker compose up --build -d
   docker compose ps
   ```

   Se algum serviço não estiver `running` ou `healthy`, veja o erro com `docker compose logs` antes de gravar.

5. Deixe o terminal aberto na pasta do projeto. Prepare abas do navegador para `http://localhost:9090` (Prometheus) e `http://localhost:16686` (Jaeger). Não mostre o conteúdo do `.env`, tokens ou senhas durante a gravação.

## Vídeo

### 0:00–0:20 — Apresentação

**Na tela:** mostre o nome do projeto no VS Code ou o README.

**Fale:**

> “Olá! Este é o Pedidos Veloz, um projeto de demonstração para mostrar como organizar uma aplicação de pedidos em serviços separados, executar tudo localmente e preparar a aplicação para Kubernetes.”

### 0:20–0:45 — Como a aplicação está dividida

**Na tela:** mostre o desenho da arquitetura no README. Aponte para Gateway, Pedidos, Pagamentos, Estoque e PostgreSQL.

**Fale:**

> “O Gateway é a porta de entrada. Ele encaminha as chamadas para Pedidos, Pagamentos ou Estoque. Pedidos e Estoque guardam informações no PostgreSQL. Pagamentos é simulado: ele não cobra dinheiro de verdade.”

### 0:45–1:15 — Iniciar localmente

**Na tela:** no terminal, mostre o comando `docker compose up --build -d` já concluído e depois `docker compose ps`.

**Fale:**

> “Com Docker Compose, os serviços sobem juntos usando um comando. Aqui eu confiro a lista e o estado dos containers. O banco mantém os dados em um volume, e só o Gateway fica exposto para o meu computador.”

### 1:15–2:05 — Fazer um pedido e consultar estoque

**Na tela:** execute cada bloco no mesmo terminal PowerShell. Primeiro verifique a saúde da API:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Crie um pedido e mostre a resposta:

```powershell
$pedido = Invoke-RestMethod -Method Post http://localhost:5000/pedidos `
  -ContentType 'application/json' `
  -Body '{"produto":"Mouse","quantidade":2,"valor_unitario":25.50}'
$pedido | Format-List
```

Mostre o pagamento simulado usando o número do pedido criado:

```powershell
$pagamento = Invoke-RestMethod -Method Post http://localhost:5000/pagamentos `
  -ContentType 'application/json' `
  -Body (@{ pedido_id = $pedido.id; valor = 51.00 } | ConvertTo-Json)
$pagamento | Format-List
```

Consulte e reserve uma unidade do estoque:

```powershell
Invoke-RestMethod http://localhost:5000/estoque
Invoke-RestMethod -Method Post http://localhost:5000/estoque/reservas `
  -ContentType 'application/json' `
  -Body '{"produto":"Mouse","quantidade":1}'
```

**Fale:**

> “A API respondeu que está saudável. Criei um pedido, recebi o identificador e fiz uma aprovação de pagamento simulada. Depois consultei o estoque e reservei uma unidade. A reserva atualiza o banco e não permite deixar o saldo negativo.”

### 2:05–2:35 — Métricas e rastreamento

**Na tela:** abra a aba do Prometheus em `http://localhost:9090`. Mostre **Status → Targets** e os serviços coletados. Depois abra o Jaeger em `http://localhost:16686`, selecione `gateway` e busque traces recentes. Se necessário, volte ao terminal e faça mais uma chamada a `/health` antes de atualizar a busca.

**Fale:**

> “O Prometheus coleta métricas dos serviços, como volume e duração das requisições. O Jaeger mostra o caminho de uma chamada entre serviços. O OpenTelemetry envia esses traces pelo Collector. Assim fica mais fácil localizar onde uma chamada demorou ou falhou.”

### 2:35–3:10 — CI/CD e Kubernetes

**Na tela:** no VS Code, abra `.github/workflows/ci-cd.yml` e mostre rapidamente as etapas de testes, publicação no GHCR e deploy manual. Depois mostre `kubernetes/gateway.yaml` e `kubernetes/hpa.yaml`.

**Fale:**

> “A configuração de CI roda verificações e testes. Na branch principal, o fluxo constrói e publica imagens identificadas pelo commit. O deploy está preparado para ser iniciado manualmente com secrets e um runner conectado ao cluster. No Kubernetes, os manifests definem serviços, verificações de saúde, atualização gradual e escala automática por CPU.”

### 3:10–3:40 — Segurança e infraestrutura

**Na tela:** mostre `kubernetes/namespace.yaml`, `kubernetes/configmap.yaml` e a pasta `terraform/`. Não abra arquivos que possam conter credenciais.

**Fale:**

> “O namespace usa controles de segurança, e as aplicações executam sem privilégios elevados. Configurações ficam no ConfigMap; as credenciais são criadas como Secrets no deploy. O Terraform descreve uma base de EKS e espera uma VPC já existente. É um esqueleto de infraestrutura, não um ambiente que foi criado neste vídeo.”

### 3:40–4:00 — Encerramento

**Na tela:** volte ao README e mostre os comandos para executar o projeto.

**Fale:**

> “Este projeto demonstra o fluxo local, os serviços, testes, métricas, traces e configurações para Kubernetes. Pagamentos continuam simulados, e o banco e a observabilidade estão configurados para demonstração. Obrigado por assistir.”

## Depois de gravar

1. Publique o vídeo no YouTube como público ou não listado.
2. Copie o link publicado para este arquivo, para o README e para o relatório PDF prático.
3. Se não demonstrou um deploy real, mantenha a explicação no nível de configuração; não diga que a aplicação foi implantada em um cluster.
4. Para parar os containers depois da gravação, execute `docker compose down`. Não use `docker compose down -v` se quiser manter os dados locais.

**Link do vídeo:** `PENDENTE — inserir URL após gravação e publicação`
