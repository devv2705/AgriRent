# Farmer Equipment Rental Portal

![Project Logo](https://imagetolink.com/ib/u7YRfckarR.png)

This is a web application that allows farmers to rent and share farming equipment easily. Farmers can register, list their available equipment for rent, and view other farmers' equipment for rent.

## Features

- User-friendly interface for easy navigation.
- Farmers can create and manage their profiles.
- Farmers can add, edit, and delete their farming equipment available for rent.
- Other farmers can view the available equipment for rent.
- Farmers can search for specific equipment using filters.
- Secure user authentication and password reset functionality.
- Settings section for changing the password and deleting the account.

## Getting Started

To run this application locally, follow these steps:

1. Clone the repository to your local machine:

       git clone https://github.com/smitkunpara/AgriRent.git

2. Create a virtual environment and activate it:

      On macOS or Linux(run on root terminal):

       python -m venv venv
       chmod +x venv/bin/activate
       venv/bin/activate

      On Windows(run on administrative cmd):

       python -m venv venv
       venv\Scripts\activate

4. Install the required dependencies:

       pip install -r requirements.txt

5. Migrate and Run the server:

       python manage.py migrate
       python manage.py runserver

6. Access the application in your web browser at `http://localhost:8000/`.
