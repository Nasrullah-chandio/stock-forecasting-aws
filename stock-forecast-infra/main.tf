resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "stock-forecast-vpc"
  }
}
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "stock-forecast-public-subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "stock-forecast-private-subnet"
  }
}
resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "stock-forecast-private-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "stock-forecast-igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "stock-forecast-public-rt"
  }
}

resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "stock-db-subnet-group"
  subnet_ids = [
    aws_subnet.private_subnet.id,
    aws_subnet.private_subnet_2.id
  ]

  tags = {
    Name = "Stock DB Subnet Group"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "rds-access"
  description = "Allow app access to PostgreSQL"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "PostgreSQL from anywhere (temporary)"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # ⚠️ You can restrict this later
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-security-group"
  }
}
resource "aws_db_instance" "stock_db" {
  identifier             = "stock-db"
  engine                 = "postgres"
  # engine_version         = "15.2"  # Optional
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "stocks"
  username               = "pgadmin"
  password               = "Passw0rd1234!"
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name

  tags = {
    Name = "stock-forecast-postgres"
  }
}
resource "aws_instance" "bastion" {
  ami                    = "ami-0c101f26f147fa7fd"  # Amazon Linux 2 AMI (us-east-1)
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.bastion_sg.id]
  key_name               = "bastion-key"  # You'll create this key pair manually or via Terraform

  tags = {
    Name = "stock-bastion"
  }
}
resource "aws_security_group" "bastion_sg" {
  name        = "bastion-sg"
  description = "Allow SSH from your laptop"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["184.147.218.58/32"]  # Replace with your actual public IP (from curl ifconfig.me)
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bastion-sg"
  }
}
resource "aws_instance" "bastion_new" {
  ami                         = "ami-0c2b8ca1dad447f8a"  # Amazon Linux 2023 AMI in us-east-1
  instance_type               = "t2.micro"
  subnet_id                   = "subnet-02032a8b05686b522"  # Your existing public subnet
  vpc_security_group_ids      = [aws_security_group.rds_sg.id]  # Use same SG that allows port 22 + Postgres
  key_name                    = "bastion-key"  # Existing key pair name

  associate_public_ip_address = true

  tags = {
    Name = "bastion-new"
  }
}

