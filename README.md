# ProjectPulse

**ProjectPulse** is a comprehensive project management platform that facilitates the organization and tracking of team tasks. It is constructed using the Flask web framework, the Vue JavaScript library, and SQLAlchemy. It enables users to create cards for individual tasks and move them through different stages of the workflow. The platform utilizes asynchronous tasks using Celery to maintain high levels of application performance and responsiveness and uses Redis to improve performance.

## Technologies Used

- **Python**
- **Flask** (web framework)
  - Flask-Caching (extension for caching)
  - Flask-Session (extension for managing sessions)
  - Flask-RESTful (extension for building REST APIs)
  - Flask-SQLAlchemy (extension for integrating with SQL databases)
  - Flask-CORS (extension for handling Cross-Origin Resource Sharing)
- **Celery** (task queue)
- **Redis** (in-memory data store)
- **Jinja2** (template engine)
- **WeasyPrint** (library for generating PDFs)
- **UUID** (library for generating universally unique identifiers)
- **Flask-Login** (extension for handling user authentication and authorization)

## DB Schema Design

### UserModel
- `id`: Integer primary key for the user
- `name`: String representing the name of the user, must be unique and cannot be null
- `password`: String representing the password of the user, cannot be null

### ListModel
- `lid`: Integer primary key for the list
- `lname`: String representing the name of the list, must be unique and cannot be null
- `user`: Integer representing the user who owns the list, cannot be null
- `ldescription`: String representing a description of the list, can be null

### CardModel
- `cid`: Integer primary key for the card
- `cname`: String representing the name of the card, cannot be null
- `lid`: Integer representing the list that the card belongs to, cannot be null
- `user`: Integer representing the user who owns the card, cannot be null
- `cdescription`: String representing a description of the card, cannot be null
- `completed`: Boolean indicating whether the card has been completed or not, cannot be null
- `creation_date`: DateTime representing the date and time when the card was created, default is the current date and time, cannot be null
- `deadline_date`: DateTime representing the deadline for completing the card, cannot be null
- `completion_date`: DateTime representing the date and time when the card was completed, can be null

## API Design

### Authentication
- **Login**: Method for logging in a user with a specified username and password.
- **Register**: Method for registering a new user with a specified username, password, and email address.
- **Logout**: Method for logging out a user.

### Lists
- **Get Lists**: Method for retrieving all lists for a user.
- **Add List**: Method for adding a new list.
- **Update List**: Method for updating an existing list.
- **Delete List**: Method for deleting a list.

### Cards
- **Get Cards**: Method for retrieving all cards for a list.
- **Add Card**: Method for adding a new card to a list.
- **Update Card**: Method for updating an existing card.
- **Delete Card**: Method for deleting a card.

### Additional Resources
- **CardPending**: Method for marking a card as completed.
- **Summary**: Method for getting summary information about a user's lists and cards, cached for 20 seconds.
- **CompDate**: Method for retrieving a summary of completed cards for a particular user, including the completion date and the time taken to complete each card.
- **ListExport**: Method for exporting a user's lists to a CSV file using a background Celery task, and returning the CSV file as a download.
- **CardExport**: Method for exporting a user's cards to a CSV file using a background Celery task, and returning the CSV file as a download.

## Asynchronous Tasks
- **ltocsv Task**: Exports a user's lists to a CSV file, retrieving all the lists belonging to a particular user and writing them to a CSV file with columns for the list ID, name, user, and description.
- **ctocsv Task**: Exports a user's cards to a CSV file, retrieving all the cards belonging to a particular user and writing them to a CSV file with columns for the card ID, name, list ID, user, description, completion status, creation date, deadline date, and completion date.

## Scheduled Tasks
- Asynchronously running scheduled tasks for daily reminders and monthly reminders.

## Frontend
The frontend is built using the Vue CLI and resides in the `FRONTEND` folder in the root directory.

## Architecture and Features
- All backend-related code is in the `app.py` file except the Celery initialization and the Flask-Cache configurations, which are imported into `app.py`.
- The application includes a "forgot password" feature, which aids a registered user by sending them their password via email.

## Getting Started

To get started with ProjectPulse, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/ProjectPulse.git
    cd ProjectPulse
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    cd FRONTEND
    npm install
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory and add the required environment variables.

4. **Initialize the database**:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. **Run the application**:
    - Start the backend server:
        ```sh
        flask run
        ```
    - Start the frontend development server:
        ```sh
        npm run serve
        ```

6. **Run Celery worker**:
    ```sh
    celery -A app.celery worker --loglevel=info
    ```

7. **Run Redis server**:
    ```sh
    redis-server
    ```


