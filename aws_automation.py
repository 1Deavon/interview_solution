import boto3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from botocore.exceptions import ClientError


from botocore.exceptions import NoCredentialsError, PartialCredentialsError



# Initialize a session using AWS credentials (Make sure credentials have admin permissions)
def create_member_account(member_email,client,accout_name):
    try:

        # Create a new account in the organization
        response = client.create_account(
            Email=member_email,  # Replace with the new account email
            AccountName=accout_name,           # Replace with a desired account name
            RoleName='OrganizationAccountAccessRole',  # This is the IAM role name for administrative access
            IamUserAccessToBilling='ALLOW'          # Allows IAM users access to billing information
        )

        # Print the response
        print("Account creation initiated:")
        print(response)

    except NoCredentialsError:
        print("Error: No AWS credentials found.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials found.")
    except Exception as e:
        print(f"An error occurred: {e}")


    # Capture the CreateAccountStatusId
    status_id = response['CreateAccountStatus']['Id']

    # Poll the status until the account creation is complete
    while True:
        status_response = client.describe_create_account_status(CreateAccountRequestId=status_id)
        status = status_response['CreateAccountStatus']['State']
        if status == 'SUCCEEDED':
            print("Account created successfully.")
            break
        elif status == 'FAILED':
            print("Account creation failed.")
            break
        else:
            print("Account creation in progress...")
            time.sleep(10)

def automate_updating_payment():
    # Set up the WebDriver
    driver = webdriver.Chrome()

    # Log in to the AWS Management Console
    driver.get("https://signin.aws.amazon.com/console")
    time.sleep(10)
    driver.find_element(By.ID, "root_account_signin").click()
    time.sleep(10)
    driver.find_element(By.ID, "resolving_input").send_keys("email")
    time.sleep(10)
    driver.find_element(By.ID, "next_button").click()
    # If a security check pops up, prompt the user to complete it manually.
    input("Security check detected. Please complete the CAPTCHA or security verification and press Enter to continue...")

    # Continue the script after manual completion
    print("Security check completed. Continuing with the automation...")
    time.sleep(10)
    driver.find_element(By.ID, "password").send_keys("password")
    time.sleep(10)
    driver.find_element(By.ID, "signin_button").click()
    time.sleep(20)


    # Navigate to the billing section for payment method updates
    driver.get("https://us-east-1.console.aws.amazon.com/billing/home#/paymentpreferences/paymentmethod/add")
    time.sleep(20)
   
    # Simulate entering payment information
    #driver.find_element(By.CLASS_NAME, "awsui_input_2rhyz_3dgle_145").click()
    #driver.find_element_by_class_name("awsui_input_2rhyz_3dgle_145").send_keys("4111111111111111")  # Replace with valid details
    #driver.find_element(By.ID, "formField85-1730755152677-366").send_keys("12/25") # expiration date
    #driver.find_element(By.ID, "formField86-1730755152678-307").send_keys("123") #cvv
    #driver.find_element(By.CSS_SELECTOR, "[data-testid='card-information-panel-card-holder-name-input']").send_keys("Yufeng Duan") # name on card
    # billing address
    #driver.find_element(By.ID, "formField104-1730755152685-5606").send_keys("Yufeng Duan") #Full name
    #driver.find_element(By.ID, "trigger-content-114-1730755152690-8240").send_keys("Example City") # Country
    #driver.find_element(By.ID, "formField115-1730755152692-9700").send_keys("123123 example st") #address
    #driver.find_element(By.ID, "formField116-1730755152693-7988").send_keys("APT31") #address2 APT, suit, unit, floor, etc ... 
    #driver.find_element(By.ID, "formField118-1730755152694-9179").send_keys("Example City") #city
    #driver.find_element(By.ID, "formField119-1730755152694-7400").send_keys("New York") #state
    #driver.find_element(By.ID, "formField120-1730755152695-4904").send_keys("00001") #zipcode
    #driver.find_element(By.ID, "formField121-1730755152695-7996").send_keys("+15513706669") #phone
    #driver.find_element(By.ID, "add-credit-card-form-submit-button").click()
    # Confirm the update

    # filling out payment information
    input("filling out your payment information, hit enter when it's done...")
    # Continue the script after manual completion
    print("updating payment information completed. Continuing with the automation...")
    # Close the browser
    driver.quit()

# Function to find the account ID by email
def get_account_id_by_email(org_client,email):
    try:
        paginator = org_client.get_paginator('list_accounts')
        for page in paginator.paginate():
            for account in page['Accounts']:
                if account['Email'] == email:
                    print(f"Found account ID for email {email}: {account['Id']}")
                    return account['Id']
        print(f"No account found for email: {email}")
        return None
    except ClientError as e:
        print(f"Error retrieving account ID: {e}")
        return None
# Function to remove an account from the organization
def remove_account_from_organization(org_client,account_id):
    try:
        time.sleep(10)
        org_client.remove_account_from_organization(AccountId=account_id)
        time.sleep(20)
        print(f"Successfully removed account {account_id} from the organization.")
    except ClientError as e:
        print(f"Error removing account {account_id} from the organization: {e}")




def main():
    # Example usage
    member_email = "example@email.com"
    account_name ="yufeng_testing"
    # Create a client for AWS Organizations
    client = boto3.client('organizations')


    create_member_account(member_email,client,account_name)
    automate_updating_payment()

    client = boto3.client('organizations')
    email = 'example@email.com'  # Replace with the actual email
    # Only attempt removal if the account ID was found
    account_id = get_account_id_by_email(client,email)
    if account_id:
        remove_account_from_organization(client,account_id)
    
    
if __name__=="__main__":
    main()
