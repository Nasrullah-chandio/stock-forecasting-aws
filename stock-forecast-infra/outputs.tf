output "bastion_public_ip" {
  description = "Public IP of the Bastion EC2 host"
  value       = aws_instance.bastion.public_ip
}

output "rds_endpoint" {
  description = "Endpoint of the RDS PostgreSQL instance"
  value       = aws_db_instance.stock_db.endpoint
}
