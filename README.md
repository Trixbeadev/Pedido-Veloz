# 🚀 Pedidos-Veloz — Cloud DevOps e Microsserviços

Projeto acadêmico desenvolvido para a atividade **Cloud DevOps: Orchestrating Containers and Micro Services**, com foco em arquitetura de microsserviços, conteinerização, orquestração, CI/CD e observabilidade.

O Pedidos-Veloz simula um sistema de gerenciamento de pedidos, separando suas principais funcionalidades em serviços independentes. O projeto busca demonstrar como automatizar a execução dos serviços, facilitar a manutenção e acompanhar o funcionamento da aplicação.

## 🎥 Vídeo de apresentação

**Assista à demonstração do projeto no YouTube:**

▶️ [Clique aqui para assistir ao vídeo do Pedidos-Veloz](https://youtu.be/DndaMGAUI_I)

O vídeo apresenta a arquitetura, a execução do ambiente e as principais decisões técnicas do projeto.

## 🎯 Objetivos do projeto

- Desenvolver uma arquitetura baseada em microsserviços.
- Automatizar a inicialização do ambiente com Docker Compose.
- Utilizar PostgreSQL para persistência de dados.
- Organizar os serviços em contêineres independentes.
- Demonstrar práticas de CI/CD e configuração de pipelines.
- Explorar a orquestração com Kubernetes.
- Implementar recursos de monitoramento e tracing distribuído.
- Documentar possibilidades de escalabilidade e infraestrutura como código.

## 🏗️ Arquitetura

A aplicação é composta pelos seguintes serviços:

| Serviço | Responsabilidade |
|---|---|
| API Gateway | Receber as requisições HTTP e encaminhá-las aos serviços correspondentes. |
| Serviço de Pedidos | Criar e consultar pedidos. |
| Serviço de Pagamentos | Simular o processamento e a aprovação de pagamentos. |
| Serviço de Estoque | Consultar e controlar a disponibilidade dos produtos. |
| PostgreSQL | Armazenar os dados da aplicação. |
| Prometheus | Coletar e consultar métricas de monitoramento. |
| Jaeger | Visualizar traces distribuídos das requisições. |
| OpenTelemetry Collector | Receber e encaminhar dados de telemetria. |

### Fluxo da aplicação

1. O cliente envia uma requisição ao API Gateway.
2. O Gateway encaminha a solicitação ao serviço responsável.
3. O serviço de pedidos interage com os demais serviços conforme a operação solicitada.
4. O pagamento é processado pela simulação implementada no serviço de pagamentos.
5. O serviço de estoque verifica ou realiza a reserva dos produtos.
6. Os dados necessários são armazenados no PostgreSQL.
7. As ferramentas de observabilidade permitem acompanhar métricas e traces da aplicação.

## 🛠️ Tecnologias utilizadas

- **Docker:** conteinerização dos serviços.
- **Docker Compose:** inicialização e organização do ambiente local.
- **Python:** desenvolvimento dos serviços da aplicação.
- **PostgreSQL:** banco de dados relacional.
- **Kubernetes:** configuração da orquestração dos contêineres.
- **GitHub Actions:** automação de etapas do pipeline CI/CD.
- **Prometheus:** monitoramento de métricas.
- **Jaeger:** visualização de tracing distribuído.
- **OpenTelemetry:** instrumentação e encaminhamento de telemetria.
- **Terraform:** infraestrutura como código.

## 📋 Pré-requisitos

Para executar o ambiente local, é necessário ter instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git
- Um terminal, como o PowerShell ou o terminal integrado do VS Code.

O Docker Desktop deve estar aberto e funcionando antes de iniciar a aplicação.

## ▶️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta do projeto:

```bash
cd Pedidos-Veloz
```

### 2. Configurar as variáveis de ambiente

Verifique o arquivo `.env.example` e configure as variáveis necessárias conforme as instruções do projeto.

Caso a aplicação exija um arquivo `.env`, crie-o a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Preencha os valores necessários antes de iniciar os serviços.

**Importante:** não publique senhas, tokens ou outras credenciais reais no repositório.

### 3. Iniciar os serviços

Na pasta que contém o arquivo `docker-compose.yml`, execute:

```bash
docker compose up --build -d
```

Esse comando constrói as imagens necessárias e inicia os serviços definidos no Docker Compose.

### 4. Verificar os contêineres

```bash
docker compose ps
```

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para encerrar o ambiente:

```bash
docker compose down
```

Os dados persistidos em volumes podem ser mantidos após a parada dos contêineres. Evite utilizar `docker compose down -v` se quiser preservar os dados locais.

## 🌐 Endereços locais

Com o ambiente iniciado e as portas configuradas conforme o `docker-compose.yml`, as ferramentas de monitoramento podem ser acessadas pelos seguintes endereços:

| Ferramenta | Endereço |
|---|---|
| API Gateway | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Jaeger | http://localhost:16686 |

Os serviços internos de pedidos, pagamentos e estoque utilizam as portas configuradas no projeto. Eles podem se comunicar pela rede interna do Docker.

> Observação: acessar a raiz do Gateway não significa necessariamente que exista uma rota configurada para `/`. Utilize os endpoints definidos pela aplicação.

## 📊 Observabilidade

O projeto utiliza ferramentas de observabilidade para acompanhar o comportamento dos serviços.

### Prometheus

Permite consultar métricas e verificar a disponibilidade dos alvos monitorados.

Exemplo de consulta:

```promql
up
```

Essa consulta permite verificar o estado dos alvos configurados no Prometheus.

### Jaeger

Permite visualizar traces distribuídos e acompanhar o caminho de uma requisição entre os serviços instrumentados.

### OpenTelemetry Collector

Centraliza o recebimento e o encaminhamento de dados de telemetria, facilitando a integração com ferramentas de observabilidade.

## ☸️ Kubernetes

O projeto inclui arquivos de configuração relacionados à execução dos serviços em Kubernetes.

Essa etapa contempla recursos de orquestração e configurações voltadas à execução dos contêineres em um ambiente distribuído.

Os manifests e demais arquivos relacionados estão organizados na pasta `kubernetes/`.

Para utilizar esses recursos, é necessário ter um cluster Kubernetes disponível e o `kubectl` configurado para acessá-lo.

## 🔄 CI/CD

O repositório inclui arquivos relacionados à automação do fluxo de desenvolvimento e validação.

A proposta de CI/CD contempla etapas como:

- Construção das imagens.
- Execução de testes e validações configurados no pipeline.
- Preparação dos artefatos necessários à entrega.
- Organização do fluxo de integração e entrega contínuas.

Os workflows estão organizados na pasta `.github/workflows/`.

## 📈 Escalabilidade e infraestrutura como código

O projeto também aborda estratégias para evolução do ambiente:

- **Escalabilidade:** possibilidade de ajustar a quantidade de réplicas dos serviços conforme a demanda.
- **Estratégias de implantação:** utilização de abordagens como Rolling Update para reduzir riscos durante atualizações.
- **Terraform:** organização da infraestrutura como código, permitindo descrever recursos de forma reproduzível.

Os arquivos relacionados à infraestrutura estão organizados na pasta `terraform/`.

## 📁 Estrutura do projeto

A estrutura pode ser consultada diretamente no repositório. As principais pastas e arquivos incluem:

```text
Pedidos-Veloz/
├── .github/
│   └── workflows/
├── gateway/
├── servico-pedidos/
├── servico-pagamentos/
├── servico-estoque/
├── database/
├── kubernetes/
├── monitoring/
├── terraform/
├── tests/
├── .env.example
├── docker-compose.yml
├── relatorio-pratico.pdf
├── relatorio-teorico.pdf
└── README.md
```

A estrutura acima destaca os principais componentes esperados do projeto. Consulte os diretórios existentes no repositório para verificar os arquivos específicos de cada serviço.

## 📄 Relatórios técnicos

Os relatórios complementam a implementação e documentam as decisões tomadas durante o desenvolvimento.

- **Relatório teórico:** conceitos de microsserviços, DevOps, conteinerização, orquestração, CI/CD e observabilidade.
- **Relatório prático:** arquitetura desenvolvida, execução do ambiente, configurações e estratégias técnicas adotadas.

Os arquivos estão disponíveis na raiz do repositório:

- `relatorio-teorico.pdf`
- `relatorio-pratico.pdf`

## 🎓 Contexto acadêmico

Projeto desenvolvido como parte da atividade **Cloud DevOps: Orchestrating Containers and Micro Services**, com o objetivo de aplicar conceitos de desenvolvimento distribuído, automação, monitoramento e infraestrutura.

O desenvolvimento permitiu praticar a integração entre serviços independentes e conhecer ferramentas utilizadas em ambientes modernos de desenvolvimento e operação de aplicações.

---

**Demonstração em vídeo:** https://youtu.be/DndaMGAUI_I
