resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.ms.id

  tags = {
    Name = "${local.env}-igw"
  }
}

