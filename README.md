# interview_solution
This solution automates the process of setting up a new AWS member account, handling login with the root user, updating the payment method, and separating the account from its original organization to become a standalone account ready to join a new organization.

## install required packages
To get started, install the following packages:

brew install awsctl
pip3 install boto3
pip3 install time
brew install selenium

## Configure AWS root origanization account
Set up the AWS root organization account by running:
$aws configure
Enter the security key, which can be found in your AWS account settings.
