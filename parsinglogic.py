# Step 2: Import the 're' module, which stands for Regular Expression
import re

# This function will contain our main parsing logic
def extract_financial_data(text):
    """
    Parses email text to extract vendor, total amount, and date.
    """
    # Initialize variables with a default "not found" value
    vendor = "Not Found"
    total = "Not Found"
    
    # --- Pattern 1: Find the Total Amount ---
    # We are looking for a dollar sign $, followed by digits, a dot, and two more digits.
    # The parentheses () capture the actual number for us to use later.
    price_pattern = r"Total:\s*\$([\d,]+\.\d{2})"
    price_match = re.search(price_pattern, text)
    
    # If a match was found, get the captured group (the number itself)
    if price_match:
        total = price_match.group(1)

    # --- Pattern 2: Find the Vendor Name ---
    # We are looking for the text that comes right after "Order from:"
    # (.*) is a pattern that means "capture any character (.), any number of times (*)"
    vendor_pattern = r"Order from:\s*(.*)"
    vendor_match = re.search(vendor_pattern, text)

    # If a match was found, get the captured group (the vendor name)
    if vendor_match:
        vendor = vendor_match.group(1).strip() # .strip() removes extra whitespace

    # --- Print the results in a structured way ---
    print("--- Extracted Financial Data ---")
    print(f"Vendor: {vendor}")
    print(f"Total Amount: ${total}")
    print("------------------------------")


# This is our main program execution block
if __name__ == "__main__":
    # Step 3: Use a sample email body as our input
    # In a real app, this text would come from the Gmail script you already built.
    email_body = """
  The details of your iDEAL payment are given below.
iDEAL Transaction Overview

Amount
EUR 61,30
Recipient
NS Internationaal B.V.
NL56DEUT0265186420
From account
H Kannan
**** **** **** ***9 05
Date
13-09-2025 11:06
Transaction number
8030484838104681
Description
DNR: RGSKNPM

    """
    
    # Call our function to parse the email text
    extract_financial_data(email_body)