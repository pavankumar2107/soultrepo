resource "aws_lambda_function" "soult" {
  function_name    = "soult"
  role             = "arn:aws:iam::242201272705:role/aws_lambda_deployment_role"
  package_type     = "Image"
  image_uri        = "242201272705.dkr.ecr.ap-south-1.amazonaws.com/demofastapi:latest"
  timeout          = 30
  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.fastapi_table.name
      S3_BUCKET      = aws_s3_bucket.demo_bucket.bucket
    }
  }
}

resource  "aws_iam_role" "aws_lambda_deployment_role" {
  name = "aws_lambda_deployment_role"
  assume_role_policy = jsonencode({

    "lambda:UpdateFunctionCode",
"lambda:UpdateFunctionConfig",
"lambda:GetFunctionConfiguration",
"lambda:AddPermission",
}

resource "aws_iam_role" "lambda_exec" {
  name = "aws_lambda_deployment_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}