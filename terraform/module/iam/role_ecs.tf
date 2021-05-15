resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "EcsTaskRole-${var.app_name}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
