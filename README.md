## AWS DevOps Assessment

# Deploy infrastructure

terraform init
terraform apply

# Run tests

python test/test_script.py

# Destroy resources

terraform destroy

# Multi-region providers
define alias as "eu" for region eu-west-1
in module declare as below:  
providers = {
    aws = aws.eu
  }
