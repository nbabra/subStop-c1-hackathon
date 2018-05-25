# subStop-c1-hackathon

----------------------------------------API DOCUMENTATION-----------------------------------------------------------------
**HOMEPAGE: http://18.221.61.221:5000**
  Function:
    Displays Signup Form for subStop, makes POST request to API to create user (SEE CREATE USER POST REQUEST BELOW)
  
**CREATE USER:http://18.221.61.221:5000/createAccount**
REQUEST: POST
  BODY: {
          "username": "username",
          "customerID": "customerID",
          "phone": "phone"
         }
         
  RETURNS EMPTY JSON (STATUS CODE = 200)
  
  Function: 
    Creates user folder in S3 Bucket and creates ACCOUNT.json file in folder. ACCOUNT.json holds the rest of the json request       body as its body (eliminates "username" key & value)
    
    
**SET SUBSCRIPTIONS: http://18.221.61.221:5000/setSubscriptions**
REQUEST: POST
  BODY: {
          "username": "username", 
          "date": "date"
         }
         
  RETURNS EMPTY JSON (STATUS CODE = 200)

  Function: 
    Accesses user folder based on username and creates SUBSCRIPTION.json files for every subscription. Each SUBSCRIPTION.json       file has body with {"date": "date"}.
    
**Update Subscription: http://18.221.61.221:5000/updateSubscription**
REQUEST: POST
  BODY: {
          "username": "username",
          "subname": "subname",
          "date": "date"
         }
         
  RETURNS EMPTY JSON (STATUS CODE = 200)

  Function: 
    Accesses user folder based on username and updates contents of subname.json with body {"date": "date"}
   
**Check Subscription: http://18.221.61.221:5000/"/checkSubscription/<username>/<subname>"**
REQUEST: GET
         
  RETURNS HTML WITH DATE PARAMETER

  Function: 
    Accesses user folder based on username and contents of subname.json and returns HTML of date value held in subname.json
    

**Update Subscription: http://18.221.61.221:5000/sendText**
REQUEST: POST
  BODY: {
          "username": "username",
         }
         
  RETURNS EMPTY JSON (STATUS CODE = 200)

  Function: 
    Texts user alerting them of their unused subscriptions



