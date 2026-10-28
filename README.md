# Pedidos Veloz — Cloud DevOps MVP

Aplicacao de e-commerce demonstrativa com gateway HTTP, microsservicos de pedidos, pagamentos (simulado) e estoque, PostgreSQL, Docker Compose, Kubernetes, GitHub Actions, Prometheus e esqueleto de infraestrutura AWS EKS com Terraform.

## Arquitetura e escopo

```text
Cliente -> Gateway :5000 -> Pedidos :5001 ----+
                           Pagamentos :5002   +--> PostgreSQL
                           Estoque :5003 -----+
```

O gateway encaminha as requisicoes. Pedidos e estoque persistem seus dados no PostgreSQL; pagamentos e uma simulacao, sem cobranca externa. O estoque usa uma atualizacao SQL atomica para evitar reservas concorrentes acima do saldo. Mensageria e service mesh foram adiadas: o MVP tem poucas operacoes sincronas e quatro semanas de prazo; eventos assincronos e mTLS via mesh seriam evolucao quando houver requisitos de desacoplamento/seguranca operacional que justifiquem essa complexidade.

## Rodar localmente

Requisitos: Docker Desktop com Docker Compose v2 e, para os testes, Python 3.12+.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

O gateway fica em `http://localhost:5000`. Exemplos no PowerShell:

```powershell
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod -Method Post http://localhost:5000/pedidos `
  -ContentType 'application/json' `
  -Body '{"produto":"Mouse","quantidade":2,"valor_unitario":25.50}'
Invoke-RestMethod http://localhost:5000/estoque
Invoke-RestMethod -Method Post http://localhost:5000/estoque/reservas `
  -ContentType 'application/json' -Body '{"produto":"Mouse","quantidade":1}'
docker compose logs -f
docker compose down
```

O volume `postgres_data` mantem os dados entre reinicios. Para apagar tambem os dados locais, use `docker compose down -v` conscientemente. A rede `backend` nao publica os microsservicos nem o banco diretamente no host. Nunca use a senha de exemplo fora de um ambiente local descartavel.

## Testes

```powershell
python -m pip install -r requirements-dev.txt
python -m pip install -r gateway/requirements.txt
python -m pip install -r servico-pedidos/requirements.txt
python -m pip install -r servico-pagamentos/requirements.txt
python -m pip install -r servico-estoque/requirements.txt
python -m pytest -q
```

Os testes cobrem validacao, criacao de pedido, pagamento simulado, reserva de estoque, endpoint de metricas e falha de comunicacao do gateway. Os testes de persistencia usam conexoes simuladas; o teste integrado com PostgreSQL pode ser feito subindo o Compose.

## Containers e imagens

Cada servico tem imagem Python slim, dependencias fixadas, Gunicorn, usuario UID 10001 nao-root e cache de instalacao desativado. A Action publica quatro imagens no GitHub Container Registry (GHCR), identificadas pelo SHA do commit e pela tag `latest`. Em producao, prefira implantar pelo SHA imutavel; `latest` e apenas conveniencia para demonstracao. As imagens do GHCR sao privadas por padrao e o cluster precisa de credencial somente-leitura para pull.

## Kubernetes

Os manifests em `kubernetes/` contem namespace com Pod Security Admission `restricted`, ConfigMap, Deployments/Services, probes, limites de recursos, RollingUpdate sem indisponibilidade planejada, HPA e PostgreSQL StatefulSet com PVC. Os Secrets nao contem valores versionados: sao criados em tempo de deploy pela Action.

Para validar/aplicar num cluster autorizado:

1. Publique as imagens (merge em `main`) e ajuste `OWNER` nos manifests ao owner do GHCR, ou use o deploy manual da Action, que atualiza os nomes e tags automaticamente.
2. Execute `kubectl apply -f kubernetes/namespace.yaml`.
3. Crie `pedidos-db` com as chaves `database-url` e `postgres-password`, e `ghcr-auth` como secret `docker-registry` com permissao somente-leitura para GHCR.
4. Crie os ConfigMaps de monitoramento a partir dos arquivos versionados:

   ```powershell
   kubectl -n pedidos-veloz create configmap prometheus-config --from-file=prometheus.yml=monitoring/prometheus.yml --dry-run=client -o yaml | kubectl apply -f -
   kubectl -n pedidos-veloz create configmap otel-collector-config --from-file=config.yaml=monitoring/otel-collector.yaml --dry-run=client -o yaml | kubectl apply -f -
   ```

5. Execute `kubectl apply -f kubernetes/`.
6. Verifique `kubectl -n pedidos-veloz get pods,services,hpa` e `kubectl -n pedidos-veloz rollout status deployment/gateway`.

A HPA exige Metrics Server instalado e funcional (`kubectl top pods -n pedidos-veloz`). Prometheus, OpenTelemetry Collector e Jaeger estao incluidos nos manifests: o Prometheus coleta `/metrics`, o Collector recebe OTLP e encaminha traces ao Jaeger. O armazenamento de Prometheus no cluster e efemero; o Jaeger usa armazenamento em memoria. Logs continuam em stdout/stderr.

Para inspecionar os sinais no cluster, use `kubectl -n pedidos-veloz port-forward svc/prometheus 9090:9090` e `kubectl -n pedidos-veloz port-forward svc/jaeger 16686:16686`; os consoles ficam em `http://localhost:9090` e `http://localhost:16686`. As APIs sao iniciadas pelo `opentelemetry-instrument`, que instrumenta Flask, requests e psycopg e propaga W3C Trace Context. Em producao, substitua o armazenamento efemero por armazenamento duravel/gerenciado e dimensione/torne redundantes os componentes de observabilidade.

No Compose, `docker compose up --build -d` tambem sobe Prometheus, Collector e Jaeger. Acesse Prometheus em `http://localhost:9090` e Jaeger em `http://localhost:16686`; as portas de monitoramento ficam limitadas a loopback.

O PostgreSQL no StatefulSet e um recurso didatico de uma replica, nao HA: antes de producao real, substituir por banco gerenciado com backup, restauracao testada, criptografia e alta disponibilidade. O `LoadBalancer` do gateway tambem precisa de TLS, ingress/WAF e politicas de rede no ambiente real.

### CI/CD

`.github/workflows/ci-cd.yml` executa verificacao de sintaxe e testes em PR; em `main`, constroi e publica as quatro imagens usando `GITHUB_TOKEN`. O deploy ocorre somente quando a Action e iniciada manualmente na branch `main`, dentro do ambiente `production`. Como o endpoint EKS e privado, o job de deploy requer um runner Linux auto-hospedado, registrado com as labels `pedidos-veloz-private` e conectado a VPC do cluster. Configure nesse ambiente os secrets `KUBECONFIG`, `DATABASE_URL`, `POSTGRES_PASSWORD`, `GHCR_USERNAME` e `GHCR_PULL_TOKEN`; habilite revisao/aprovacao do ambiente no GitHub. O runner deve ter AWS CLI quando o kubeconfig usar o plugin exec do EKS; o kubeconfig deve ter permissao minima e curta duracao. O deploy atualiza as imagens para o SHA da execucao e aguarda os rollouts.

## Infraestrutura como codigo

`terraform/` define um cluster EKS com endpoint privado, logs de auditoria/controle, grupo gerenciado de nos e addons de rede/storage. A VPC e as subnets privadas sao entradas preexistentes; copie e edite `terraform/terraform.tfvars.example` como `terraform/terraform.tfvars` local (nao versionar secrets/state), configure state remoto com lock e criptografia, revise custos e rode `terraform fmt`, `terraform validate` e `terraform plan` antes de qualquer `apply`. O modulo nao provisiona VPC, banco gerenciado, DNS, TLS nem observabilidade.

## Relatorios e video

- [Relatorio teorico (PDF)](./relatorio-teorico.pdf) — arquitetura cloud-native, conteinerizacao, orquestracao, CI/CD e observabilidade.
- [Relatorio pratico (PDF)](./relatorio-pratico.pdf) — desenho e demonstracao da implementacao, deploy, escala, Terraform e limites do MVP.
- [Roteiro do pitch de ate 4 minutos](./docs/roteiro-video.md).
- **Video YouTube:** pendente de gravacao e publicacao pela equipe. Substitua `PENDENTE` no roteiro e neste README pelo link publico ou nao listado antes da entrega final; nao foi criada uma URL ficticia.

## Referencias primarias e exemplo concreto

- Kubernetes, Deployments e rollouts: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes, probes: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
- Kubernetes, HPA: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- Kubernetes, Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Docker Compose: https://docs.docker.com/compose/
- Docker build best practices: https://docs.docker.com/build/building/best-practices/
- GitHub Actions: https://docs.github.com/actions
- Terraform AWS EKS module: https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest
- OpenTelemetry: https://opentelemetry.io/docs/what-is-opentelemetry/
- 12-Factor App: https://12factor.net/
- Exemplo publico de referencia: Google Cloud [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo), um e-commerce demonstrativo composto por 11 microsservicos, executavel em Kubernetes, com documentacao de arquitetura. Serve como evidencia concreta de decomposicao e operacao cloud-native, nao como prova de resultados de producao.
