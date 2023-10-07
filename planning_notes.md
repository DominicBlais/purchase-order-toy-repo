# Project Planning notes

## Project Specification (Given at Start)

> Your task is to implement a feature which allows employees to bulk insert purchase order information. To demonstrate the feature, you need to build a minimal app, which includes a front-end web interface and a back-end API service.
>
> The application should have a form that allows employees to submit the purchase order details. The required form fields are date, vendor name and a file that accepts a CSV containing the following required information: "Model Number, Unit Price, Quantity". The form will be submitted to the backend and the application should display either a success message or any validation errors that occurred.
>
> The backend service should parse the CSV and form elements and relay any validation errors to the frontend. The uploaded file requires Model Number to be a string, Unit Price to be a float/decimal, and Quantity should be an integer. Valid submissions should have all data persisted to your choice of storage.
>
> Feel free to implement any additional business rules you see appropriate. If you decided to add anything, please explain your reasoning.
>
> For this coding exercise, you are allowed to use any programming languages, frameworks, and tools.
>
> A submitted solution should be runnable without configuration, modifying code or computer settings, e.g. Docker, Heroku, etc.
>
> The code should be ubmitted to GitHub so that we can look at the commit history and validate your knowledge of Git. The first commit should only contain a README.md file containing a time estimate for completion of this exercise. It should be done immediately upon starting this exercise.

## Initial Brainstorm

Okay... so this will obviously need two parts, a frontend and a backend. I want to demonstrate proficiency in technologies I'm guessing are relevant to the company. From the CoderByte challenges, I think this includes Python, JavaScript, SQL, and React. This immediately suggests a Python backend and a React frontend.

Diving deeper, I'll use a relational database for the requirement to persist the data. The data structure here is very simple and there is no requirement for complex queries, etc. All in all, I think I will keep the technology for the data system simple to match, so probably no ORM. For the db itself, I think sqlite will be just fine. If I didn't know the company likes SQL, I would consider even simpler approaches like a key-value database, but this seems like a good fit for the project.

For the server business side there are lots of options, e.g. Django, Flask, Pyramid, etc. But I don't need a lot of fancy features here and am most concerned with the "API service" element. I think FastAPI would be a good fit for this. The only thing is that I don't want to run a separate server or system for static files, so that's a little stretch from FastAPI's typical use. Looks like there's a reasonable StaticFiles feature for FastAPI, so that'll work.

Now, I think I will initially approach this purely from the server side, getting the API done. Two tiny details stand out here: the need to upload a file and testing to see if the data is correct. It's easy enough to upload a file with curl, so that's no problem, but I think I need to extend the feature set a little past the specifications minimum:

#### Note: Adding a get purchase order details function to the API, so I can easily examine the results in the database.

Okay, I think I have enough information to get started. I'll divide the project into two directories, one for the Python and one for the JS. I'll start by standing up a simple FastAPI server and add a couple functions for uploading and retrieving the po details. Hmm... I think I'll also add a function to clear the database.

#### Note: Adding a reset database function to the API so I can test from a clean slate.

This brings up testing. I think I'll address that next after standing up the FastAPI server. So, the relevant api will be built on the /po directory and look like this:
- po/get_order_details
- po/upload_order_details
- po/reset_database

I'll return at least a simple JSON status for each of these. I'm going to start adding unit tests for these, checking these statuses. I'll expand this out later for the validation of the input form.

#### Note: Adding a shutdown server API call to make it easier to test.

Okay, I think the database code should come next. While all the data could be squashed into one table, is this was an actual application, this almost certainly would be two (or more) tables: one for the order details and one for vendor/order information. I'm going to do it with two tables, especially as I think it'd be practical to grab the "free" data of the upload time and uploader IP address.

So, the order table:
- id
- vendor_name
- order_date
- upload_date
- upload_ip_address

And then the details table would be something like:
- id
- model_number
- unit_price
- quantity
- (foreign key) order_id

Hmm... as sqlite3 doesn't have a fixed decimal/currency datatype, I think I'll store it as pennies to avoid an "Office Space" situation. I know JavaScript doubles are reasonably safe from currency bitrot, but scar tissue tells me this is good practice in case the database is ever used by something else (spoiler alert: it won't be). So, I'll call it unit_price_cents to be more clear.

I'm going to store the database in a little "db" subdirectory off of the python module.

Alright, last part of the server: the upload CSV function. The spec says to validate the CSV on the backend and send validation errors up to the client (along with empty vendor_name or order_date). This should be reasonably straight-forward. I'll create a couple test CSV files as well.

Hmm... one decision is whether to completely reject a CSV file if any of it is invalid, or to allow the valid rows to be added. I think I'll just kick the whole thing back if there are any errors, since it's always a pain to undo a typo otherwise.

For validation I will check to make sure the types are right and that there are a correct number of columns. I think I will check if the first row is a header and allow that if so.

Just remembered that FastAPI's docs include a built-in function test apparatus. Such a nice feature.

Okay, low on time. Going to use React with... antd. Should be pretty fast. It's TS, but that will work fine. Got to move on it now.
