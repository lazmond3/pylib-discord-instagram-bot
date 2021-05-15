# プライベートサブネットの登録を忘れていた
# Private Subnet
resource "aws_subnet" "privates" {
  count = length(var.vpc_private_subnet_cidrs)

  vpc_id = aws_vpc.main.id

  availability_zone = var.vpc_azs[count.index]
  cidr_block        = var.vpc_private_subnet_cidrs[count.index]

  tags = {
    Name = "${var.app_name}-private-${count.index}"
  }
}

resource "aws_route_table" "privates" {
  count = length(var.vpc_private_subnet_cidrs)

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.app_name}-private-${count.index}"
  }
}
resource "aws_route_table_association" "privates" {
  count = length(var.vpc_private_subnet_cidrs)

  subnet_id      = element(aws_subnet.privates.*.id, count.index)
  route_table_id = element(aws_route_table.privates.*.id, count.index)
}
