# Coding challenge Chigago Taxi 

This was a codinn challenge presented around ingesting the Chicago Taxi Ride data set. 

Work in progress. 

Basic stack 

- AWS CDK for insfrastructure as code
- SQL data models DBT 
- API Python Flask 

What code does what:
- Data api -> flask_app
- AWS iaC -> bin, lib
- DBT models for SQL data cleaning -> dbt_model
- Fetching data from Taxi API -> data_in
- Putting data into DynamoDB -> dynamo_put
- Tests -> test
