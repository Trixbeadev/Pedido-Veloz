variable "aws_region" {
  description = "Regiao AWS onde o cluster sera provisionado."
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Nome do cluster EKS."
  type        = string
  default     = "pedidos-veloz"
}

variable "kubernetes_version" {
  description = "Versao suportada pelo EKS no ambiente alvo."
  type        = string
  default     = "1.34"
}

variable "vpc_id" {
  description = "VPC previamente criada para o cluster."
  type        = string
}

variable "private_subnet_ids" {
  description = "Subnets privadas em pelo menos duas zonas de disponibilidade."
  type        = list(string)

  validation {
    condition     = length(var.private_subnet_ids) >= 2
    error_message = "Informe ao menos duas subnets privadas em zonas distintas."
  }
}

variable "node_instance_types" {
  description = "Tipos de instancia para o grupo gerenciado."
  type        = list(string)
  default     = ["t3.large"]
}

variable "node_min_size" {
  description = "Numero minimo de nos."
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Numero maximo de nos."
  type        = number
  default     = 6
}

variable "node_desired_size" {
  description = "Numero inicial desejado de nos."
  type        = number
  default     = 2
}