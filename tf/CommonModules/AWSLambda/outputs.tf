# output "rolename" {
#   value = { for i, j in aws_iam_role.AllRoles : j.name => j.name }
# }

output "rolearn" {
  value = [for i, j in aws_lambda_function.test_lambda : j.arn]
}