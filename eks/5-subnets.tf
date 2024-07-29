resource "aws_subnet" "private_zone_1" {
  vpc_id            = aws_vpc.ms.id
  cidr_block        = var.pri_sub_a
  availability_zone = local.zone1

  tags = {
    "Name"                                    = "${local.env}-private-${local.zone1}"
    "kubernetes.io/role/internal-elb"         = "1"
    "kubernetes.io/cluster/${local.eks_name}" = "owned"
  }

}

resource "aws_subnet" "private_zone_2" {
  vpc_id            = aws_vpc.ms.id
  cidr_block        = var.pri_sub_b
  availability_zone = local.zone2

  tags = {
    "Name"                                    = "${local.env}-private-${local.zone2}"
    "kubernetes.io/role/internal-elb"         = "1"
    "kubernetes.io/cluster/${local.eks_name}" = "owned"
  }

}

resource "aws_subnet" "public_zone_1" {
  vpc_id                  = aws_vpc.ms.id
  cidr_block              = var.pub_sub_a
  availability_zone       = local.zone1
  map_public_ip_on_launch = true
  tags = {
    "Name"                                    = "${local.env}-public-${local.zone1}"
    "kubernetes.io/role/elb"                  = "1"
    "kubernetes.io/cluster/${local.eks_name}" = "owned"
  }


}

resource "aws_subnet" "public_zone_2" {
  vpc_id                  = aws_vpc.ms.id
  cidr_block              = var.pub_sub_b
  availability_zone       = local.zone2
  map_public_ip_on_launch = true
  tags = {
    "Name"                                    = "${local.env}-public-${local.zone2}"
    "kubernetes.io/role/elb"                  = "1"
    "kubernetes.io/cluster/${local.eks_name}" = "owned"
  }

}