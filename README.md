# 🚀 Pedido-Veloz — Cloud DevOps e Microsserviços

Projeto acadêmico desenvolvido para a atividade **Cloud DevOps: Orchestrating Containers and Micro Services**, com foco em arquitetura de microsserviços, conteinerização, orquestração, integração e entrega contínuas (CI/CD) e observabilidade.

O Pedido-Veloz simula um sistema de gerenciamento de pedidos, separando suas principais funcionalidades em serviços independentes. O projeto busca demonstrar como organizar a aplicação em microsserviços, automatizar a execução dos serviços e acompanhar o funcionamento do ambiente.

## 🎥 Vídeo de apresentação

**Assista à demonstração do projeto no YouTube:**

▶️ [Clique aqui para assistir ao vídeo do Pedido-Veloz](https://youtu.be/DndaMGAUI_I)

O vídeo apresenta a demonstração do projeto e suas principais funcionalidades.

## 🎯 Objetivos do projeto

- Desenvolver uma arquitetura baseada em microsserviços.
- Automatizar a inicialização do ambiente utilizando Docker Compose.
- Utilizar PostgreSQL para persistência de dados.
- Organizar os serviços em contêineres independentes.
- Trabalhar com práticas de integração e entrega contínuas (CI/CD).
- Explorar a orquestração de contêineres com Kubernetes.
- Utilizar ferramentas de monitoramento e rastreamento distribuído.
- Conhecer estratégias de escalabilidade e infraestrutura como código.

## 🏗️ Arquitetura

A aplicação está organizada em serviços independentes, com responsabilidades específicas dentro do sistema de gerenciamento de pedidos.

| Componente | Responsabilidade |
|---|---|
| Portal / API Gateway | Ponto de entrada para as requisições da aplicação, conforme a implementação do projeto. |
| Serviço de Pedidos | Responsável pelas operações relacionadas aos pedidos. |
| Serviço de Pagamentos | Responsável pela lógica de pagamentos implementada no projeto. |
| Serviço de Estoque | Responsável pelas operações relacionadas ao estoque. |
| Banco de dados | Armazenamento das informações utilizadas pela aplicação. |
| Prometheus | Monitoramento de métricas, conforme a configuração do ambiente. |
| Jaeger | Visualização de rastreamentos distribuídos, conforme a instrumentação configurada. |
| OpenTelemetry | Instrumentação e encaminhamento de dados de telemetria, conforme a implementação. |

### Fluxo da aplicação

De maneira geral, o fluxo de uma aplicação de gerenciamento de pedidos baseada em microsserviços pode envolver as seguintes etapas:

1. O cliente acessa a aplicação.
2. A requisição é encaminhada ao componente responsável por recebê-la.
3. O serviço de pedidos executa a operação solicitada.
4. Os serviços de pagamentos e estoque participam das operações que necessitam dessas funcionalidades.
5. As informações necessárias são armazenadas no banco de dados.
6. As ferramentas de observabilidade auxiliam no acompanhamento do ambiente, quando configuradas para isso.

O fluxo exato depende das rotas, das integrações e das configurações implementadas nos serviços.

## 🛠️ Tecnologias utilizadas

As tecnologias relacionadas ao projeto incluem:

- **Docker:** conteinerização dos serviços.
- **Docker Compose:** organização e inicialização do ambiente local.
- **Python:** desenvolvimento dos serviços de aplicação.
- **PostgreSQL:** banco de dados relacional.
- **Kubernetes:** orquestração de contêineres.
- **GitHub Actions:** automação de etapas do pipeline CI/CD.
- **Prometheus:** monitoramento de métricas.
- **Jaeger:** visualização de rastreamentos distribuídos.
- **OpenTelemetry:** instrumentação e encaminhamento de telemetria.
- **Terraform:** infraestrutura como código.

A utilização efetiva de cada tecnologia depende dos arquivos e das configurações presentes no repositório.

## 📋 Pré-requisitos

Para preparar o ambiente local, são necessários:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git
- Um terminal, como o PowerShell ou o terminal integrado do VS Code.

O Docker Desktop deve estar instalado, aberto e funcionando antes de iniciar os contêineres.

## ▶️ Como executar o projeto

### 1. Clonar o repositório

Execute o comando:

```bash
git clone https://github.com/Trixbeadev/Pedido-Veloz.git
```

Entre na pasta do projeto:

```bash
cd Pedido-Veloz
```

### 2. Configurar as variáveis de ambiente

O repositório possui o arquivo `.env.exemplo`.

Confira as variáveis disponíveis nesse arquivo e verifique quais são necessárias para executar a aplicação.

Se o projeto exigir um arquivo `.env`, crie uma cópia do exemplo pelo PowerShell:

```powershell
Copy-Item .env.exemplo .env
```

Depois, preencha os valores necessários conforme a configuração dos serviços.

**Importante:** não publique senhas, tokens ou outras credenciais reais no repositório.

### 3. Iniciar os serviços

Na pasta que contém o arquivo `docker-compose.yml`, execute:

```bash
docker compose up --build -d
```

Esse comando solicita ao Docker Compose a construção das imagens necessárias e a inicialização dos serviços definidos na configuração.

### 4. Verificar os contêineres

Para verificar o estado dos serviços, execute:

```bash
docker compose ps
```

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para encerrar os serviços:

```bash
docker compose down
```

A parada dos contêineres não remove necessariamente os volumes de dados. Evite utilizar `docker compose down -v` se quiser preservar os dados armazenados nos volumes locais.

> **Observação:** a execução correta depende das configurações presentes no `docker-compose.yml` e das variáveis de ambiente exigidas pela aplicação.

## 🌐 Endereços locais

Depois de iniciar o ambiente, os serviços poderão ser acessados pelas portas definidas no arquivo `docker-compose.yml`.

Caso estejam configuradas com as portas abaixo, os endereços serão:

| Ferramenta | Endereço |
|---|---|
| Portal / API Gateway | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Jaeger | http://localhost:16686 |

Esses endereços dependem do mapeamento de portas definido no Docker Compose.

Os serviços internos de pedidos, pagamentos e estoque podem se comunicar pela rede interna do Docker, conforme a configuração do ambiente.

> **Observação:** acessar a raiz do portal ou do Gateway não significa necessariamente que exista uma rota configurada para `/`. Utilize os endpoints definidos pela aplicação.

## 📊 Observabilidade

A observabilidade permite acompanhar o comportamento dos serviços e identificar possíveis problemas durante a execução da aplicação.

### Prometheus

O Prometheus é uma ferramenta utilizada para coletar e consultar métricas de monitoramento.

Quando configurado, permite verificar as métricas dos alvos monitorados.

Exemplo de consulta:

```promql
up
```

Essa consulta permite verificar o estado dos alvos configurados no Prometheus.

### Jaeger

O Jaeger permite visualizar rastreamentos distribuídos e acompanhar o caminho das requisições entre serviços instrumentados.

### OpenTelemetry

O OpenTelemetry oferece recursos para instrumentação e geração de dados de telemetria, facilitando o acompanhamento das operações realizadas pela aplicação.

A coleta e a visualização desses dados dependem da instrumentação e das configurações presentes no projeto.

## ☸️ Kubernetes

O repositório possui uma pasta chamada `Kubernetes`, destinada aos arquivos relacionados à orquestração dos contêineres.

O Kubernetes permite organizar a execução de aplicações conteinerizadas e oferece recursos para gerenciamento de serviços, réplicas e atualizações.

Para utilizar os recursos do projeto, é necessário ter um cluster Kubernetes disponível e o `kubectl` configurado para acessá-lo.

Os procedimentos específicos de execução dependem dos manifests e das configurações existentes na pasta `Kubernetes`.

## 🔄 CI/CD

O projeto aborda práticas de integração e entrega contínuas (CI/CD), que permitem automatizar etapas do processo de desenvolvimento e validação de aplicações.

Entre as atividades que podem fazer parte desse processo estão:

- Construção das imagens dos serviços.
- Execução de testes e validações automatizadas.
- Verificação das alterações realizadas no código.
- Preparação dos artefatos necessários para a entrega.

Os arquivos de automação relacionados ao GitHub Actions ficam normalmente organizados em `.github/workflows/`.

A execução efetiva dessas etapas depende dos workflows configurados no repositório.

## 📈 Escalabilidade e infraestrutura como código

O projeto também aborda conceitos relacionados à evolução e à manutenção de ambientes baseados em microsserviços.

### Escalabilidade

A escalabilidade permite ajustar a capacidade de execução da aplicação conforme a demanda. Em ambientes compatíveis, isso pode envolver o aumento ou a redução da quantidade de réplicas dos serviços.

### Estratégias de implantação

Estratégias como Rolling Update permitem realizar atualizações graduais das aplicações, reduzindo os riscos associados à substituição de versões.

### Terraform

O Terraform é uma ferramenta de infraestrutura como código que permite descrever e gerenciar recursos de infraestrutura por meio de arquivos de configuração.

Os arquivos relacionados a essa parte do projeto estão organizados na pasta `terraformar`.

A aplicação efetiva dessas estratégias depende das configurações implementadas nos arquivos do projeto.

## 📁 Estrutura do projeto

O repositório está organizado nas seguintes pastas e arquivos principais:

```text
Pedido-Veloz/
├── .github/
├── banco de dados/
├── portal/
├── Kubernetes/
├── monitoramento/
├── serviço-estoque/
├── serviço-pagamentos/
├── serviço-pedidos/
├── terraformar/
├── testes/
├── .env.exemplo
├── .gitignore
├── docker-compose.yml
└── README.md
```

Essa estrutura apresenta os diretórios e arquivos identificados no repositório. Cada pasta reúne os arquivos relacionados à sua respectiva finalidade.

## 📄 Relatórios técnicos

Os relatórios técnicos complementam a documentação do projeto e apresentam os conceitos estudados, a arquitetura desenvolvida e as decisões adotadas durante a implementação.

- **Relatório teórico:** aborda os conceitos relacionados a microsserviços, DevOps, conteinerização, orquestração, CI/CD e observabilidade.
- **Relatório prático:** documenta a implementação do projeto, as ferramentas utilizadas e as configurações realizadas.

Os relatórios devem ser consultados no local definido para a entrega acadêmica, pois seus arquivos não foram identificados na raiz do repositório.

## 🎓 Contexto acadêmico

Projeto desenvolvido como parte da atividade **Cloud DevOps: Orchestrating Containers and Micro Services**, com o objetivo de aplicar conceitos de desenvolvimento distribuído, conteinerização, automação, monitoramento e infraestrutura.

O desenvolvimento proporciona a oportunidade de estudar a integração entre serviços independentes e conhecer ferramentas utilizadas em ambientes modernos de desenvolvimento e operação de aplicações.

---

**Vídeo de apresentação:** https://youtu.be/DndaMGAUI_I

**Repositório:** https://github.com/Trixbeadev/Pedido-Veloz
