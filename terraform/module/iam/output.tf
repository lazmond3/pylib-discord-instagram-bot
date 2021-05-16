output "aws_iam_role_ecs_task_execution_role_id" {
  value = aws_iam_role.ecs_task_execution_role.id
}
output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}
