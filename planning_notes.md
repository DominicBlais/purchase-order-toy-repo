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

This brings up testing. I think I'll address that next after standing up the FastAPI server.

