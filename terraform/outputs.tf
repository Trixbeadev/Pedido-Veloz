output "cluster_name" {
  description = "Nome do cluster EKS criado."
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint privado da API do cluster."
  value       = module.eks.cluster_endpoint
}

output "cluster_arn" {
  description = "ARN do cluster EKS criado."
  value       = module.eks.cluster_arn
}