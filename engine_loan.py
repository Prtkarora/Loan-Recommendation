import os
from openai import OpenAI
import pandas as pd

client = OpenAI(
    api_key="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",
)


#import data
loan_list = pd.read_csv('Loan_Comparison_Table - Sheet1.csv')
user_data = pd.read_csv('UserDataLoan4.csv')


# Define a function to find the best match
def find_best_match(row, loan_list):
    # Construct the prompt
    # prompt = f"Find the credit card names of 5 best matches in decreasing priority for the following row in the second dataset: {row.to_dict()}\nSecond dataset:\n{loan_list.to_dict(orient='records')}\n"
    
    prompt = f"""
Analyze the following user input data: {row.to_dict()} and the list of available loan options: {loan_list.to_dict(orient='records')}

in input data: {row.to_dict()} - 
If the user is specifically requesting funds to "buy a new Home", suggest him a home loan,
If the user is specifically requesting funds to "buy a new Car", suggest him a New Car Loan,
If the user is specifically requesting funds to "buy a used Car", suggest him a Used Car Loan.

Return the response in the following JSON format:

{{
    "totalMatches": 1,
    "matches": [
        {{
            "rank": 1,
            "Loan Type": "Loan_Type",
            "Loan Type Category": "Loan_Type_Category",
            "Interest Rate": "Interest_Rate_Range",
            "Processing Fees": "Processing_Fees",
            "Minimum Tenure": "Minimum_Tenure",
            "Maximum Tenure": "Maximum_Tenure",
            "Maximum Loan Amount": "Maximum_Loan_Amount",
            "Minimum Loan Amount": "Minimum_Loan_Amount",
            "Security Required": "Security_Required",
            "Credit Score Requirement": "Credit_Score_Requirement",
            "Minimum Income": "Minimum_Income",
            "FOIR Requirement": "FOIR_Requirement",
            "reason": "Personalized_reason_for_recommendation"
        }}
    ]
}}

Otherwise, strictly give the top 3 most suitable loans based on matching criteria weighing these columns from: {loan_list.to_dict(orient='records')} on the priority order of:
    - Funds Needed For
    - Collateral Required
    - Minimum Loan Amount
    - Tenure
    - Employment Type
    - Credit Score, FOIR, and Minimum Income are equally weighted for the closest match in descending order, with user input data: {row.to_dict()}
    For example: Give more preference to Home Loan Top-up and Loan against Property if the user has home as available collateral

    Important note: If the collateral is provided in the user input (Shares / Mutual Funds), give more preference to the (Loan againt shares / Loan against Mutual Funds) loans over other loans

{{
    "totalMatches": 3,
    "matches": [
        {{
            "rank": 1,
            "Loan Type": "Loan_Type",
            "Loan Type Category": "Loan_Type_Category",
            "Interest Rate": "Interest_Rate_Range",
            "Processing Fees": "Processing_Fees",
            "Minimum Tenure": "Minimum_Tenure",
            "Maximum Tenure": "Maximum_Tenure",
            "Maximum Loan Amount": "Maximum_Loan_Amount",
            "Minimum Loan Amount": "Minimum_Loan_Amount",
            "Security Required": "Security_Required",
            "Credit Score Requirement": "Credit_Score_Requirement",
            "Minimum Income": "Minimum_Income",
            "FOIR Requirement": "FOIR_Requirement",
            "reason": "Personalized_reason_for_recommendation",
            "match_score": Match_Score
        }},
        {{
            "rank": 2,
            "Loan Type": "Loan_Type",
            "Loan Type Category": "Loan_Type_Category",
            "Interest Rate": "Interest_Rate_Range",
            "Processing Fees": "Processing_Fees",
            "Minimum Tenure": "Minimum_Tenure",
            "Maximum Tenure": "Maximum_Tenure",
            "Maximum Loan Amount": "Maximum_Loan_Amount",
            "Minimum Loan Amount": "Minimum_Loan_Amount",
            "Security Required": "Security_Required",
            "Credit Score Requirement": "Credit_Score_Requirement",
            "Minimum Income": "Minimum_Income",
            "reason": "Personalized_reason_for_recommendation",
            "match_score": Match_Score
        }}
    ]
}}

Ensure the output is always in valid JSON format and follows these guidelines:
- Always return exactly 3 matches if applicable.
- Include a numeric match score (0-100) to rank the best loan options.
- Prioritize matching based on:
    - Funds Needed For
    - Security Required
    - Minimum Loan Amount
    - Tenure
    - Employment Type
    - Credit Score, FOIR, and Minimum Income are equally weighted.
- Use decimal precision for match scores.
- Provide a specific and personalized reason for each loan recommendation.
- Respond strictly in JSON format with no additional text or explanations.
"""


    
    # Call the OpenAI API
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        },
    ],
    max_tokens=1200,
    temperature=0.1,
    model="gpt-3.5-turbo"
    )


    # Extract the result
    result = response.choices[0].message.content
    return result
    


#Iterate through user_data and find the best match in loan_list
matches = []
for index, row in user_data.iterrows():
    best_match = find_best_match(row, loan_list)
    matches.append(best_match)

#Print the matches
for match in matches:
    print(match)