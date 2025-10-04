# Fun Fact Generator Web App

The Fun Fact Generator Web App is an interactive platform that delivers random, interesting, and educational facts to users. Unlike traditional console-based programs, this app provides a modern web interface where users can explore facts by categories such as Science, History, and Technology.This project combines frontend interactivity (Streamlit), backend API handling (FastAPI), and database management (Supabase) to create a fun, educational, and user-friendly web application.

## Features

_**Random Fact Generation**: Users can click a button to instantly receive a new fun fact.

_**User Registration & Login**: Secure user authentication for personalized experiences.

_**Favorites Management**: Users can save their favorite facts for easy access.

_**Category-Based Fact Discovery**: Explore facts by categories such as Science, History, and Technology.

_**Share Your Own Facts**: Users can contribute by adding their own fun facts to the platform

## Project Structure

FUN_FACTS_GENERATOR/
|
|---src/            # core application logic
|    |---logic.py   # business logic and task
operations
|    |__db.py       # Database operations
|
|---api/            # Backend API
|   |__main.py      # FastAPI endpoints
|
|---frontend/       # Frontend application
|    |__app.py      # streamlit web interface
|
|___requirements.txt    # Python Dependencies
|
|___README.md       # Project documentation
|
|___.env            # Python Variables 


## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,cloning)

### 1. Clone or Download the Project
# Option 1: Clone with Git
git clone <repository-url>

# Option 2: Download and extract the ZIP file

### 2. Install Dependencies

# Install all required Python packages
pip install -r requirements.txt

### 3. Set Up Supabase Database

1.Create a Supabase Project:

2.Create the Tasks Table:
- Go to the SQL Editor in your supabase dashboard
- Run this SQL command:

``` sql
CREATE TABLE usersdata (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username text UNIQUE NOT NULL,
    email text UNIQUE NOT NULL,
    password_hash text NOT NULL,
    created_at timestamp DEFAULT now()
);


CREATE TABLE fun_facts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    category text NOT NULL,
    fact_text text NOT NULL,
    created_by uuid REFERENCES usersdata(id) ON DELETE SET NULL,
    created_at timestamp DEFAULT now()
);



CREATE TABLE user_favorites (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES usersdata(id) ON DELETE CASCADE,
    fact_id uuid NOT NULL REFERENCES fun_facts(id) ON DELETE CASCADE,
    favorited_at timestamp DEFAULT now(),
    UNIQUE(user_id, fact_id)
);

ALTER TABLE fun_facts ADD COLUMN source TEXT DEFAULT 'manual';

```
### 3. **Get Your Credentials**

### 4. Configure Environment Variables

1. Create a `.env` file in the project root

2. Add your Supabase credentias to `.env` :
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here


**Example:**
SUPABASE_URL='https://xcfhedwabzklgfajogok.supabase.co'
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjZmhlZHdhYnprbGdmYWpvZ29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODI0NzIsImV4cCI6MjA3MzY1ODQ3Mn0.FRSN6wzJPBY2W4-CSx5UWLw1_4pUAZbS5iNhn7Dobis"

### 5. Run the Application

## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

## FastAPI Backend

cd api
python main.py

The API will be available at `http://localhost:8000`

## How to use
**Register / Login**

Open the Streamlit app (http://localhost:8501)

Click Register to create a new account or Login if you already have one.

**Discover Fun Facts**

Browse fun facts by category.

Click Add to Favorites to save interesting facts.

Click Generate Fact to fetch a random fact using API Ninjas. It will automatically be saved in the database with category “Random Fun Fact”.

**Add Fun Facts**

Use the Add Fun Fact page to contribute your own facts with a category.

The fact is stored in the Supabase database.

**Favorites**

Go to My Favorites to view all saved fun facts.

## Technical Details

### Technologies Used

_ **Frontend**: Streamlit (Python web framework)
_ **Backend**: FatsAPI  (Python REST API frameworks)
_ **Database**: Supabase (PostgreSQL-based backend-as-a-service)
_ **Language**: Python 3.8+

### Key Components

1._**src/db.py**: Database operations – Handles all CRUD operations with Supabase (users, fun facts, favorites).

2._**src/logic.py**: Business logic – Handles validation, password hashing, and processing before interacting with the database.

3._**api/main.py**: API endpoints – Defines all REST API routes for user authentication, CRUD operations for facts, favorites, and random fact generation via API Ninjas.

4._**app.py**: Frontend – Streamlit app handling the user interface, pages for registration, login, discovering facts, adding facts, generating random facts, and viewing favorites.

5._**.env**: Environment variables – Stores Supabase credentials and API keys securely.

6._**requirements.txt**: Dependencies – Lists all Python libraries needed for backend and frontend.

7._**README.md**: Project documentation – Explains setup, usage, technical details, technologies used, and key components.

## Troubleshooting


If you face problems while running the project, here are practical solutions based on my experience:

1.**FastAPI backend not running or connection refused**

Cause: Backend is not started or running on a different port.

Solution: Start the backend using:

uvicorn api.main:app --reload --port 8000


Ensure the URL in BASE_URL in app.py matches (http://localhost:8000).

2.**Environment variables not loaded properly**

Cause: .env file missing or keys incorrect.

Solution: Check that .env contains:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
API_NINJAS_KEY=your_api_ninjas_key


Then restart the backend.

3.**API-Ninjas fact generation fails**

Cause: Invalid API key or network issues.

Solution: Make sure API_NINJAS_KEY is valid and has not exceeded rate limits.

4.**Facts not displayed on Streamlit**

Cause: Backend API not reachable or empty database.

Solution: Ensure the backend is running and fun_facts table in Supabase has data.

5.**Login fails even with correct credentials**

Cause: Password mismatch due to hashing issues.

Solution: Make sure passwords are hashed when registering and check that login verifies with bcrypt.

6.**Favorites not working**

Cause: Backend not storing user_favorites correctly or duplicate entries.

Solution: Favorites are now checked for duplicates; clear the table in Supabase if corrupted and retry.

## Common Issues

**No categories appear in Discover Facts dropdown**

    Only existing fact categories are shown. Add some facts first for categories to appear.

**Generate Fact does not create category-based fact**

    We decided to generate only “Random Fun Fact” category to simplify usage. Category field removed in Streamlit UI.

**Supabase insert/update returns None**

    Cause: Empty response from Supabase insert/update.

    Solution: Ensure res.data[0] exists after insertion. Tables must have correct columns.

**Streamlit UI freezes or shows empty page**

    Clear Streamlit session state and cache:

    streamlit cache clear

    Then restart Streamlit.

## Future Enhancements

--**User Authentication & Profiles**

Add signup/login functionality with email or social accounts.

Personalized dashboards to track favorite facts, submitted facts, and activity history.

--**Admin Panel for Fact Moderation**

Allow admins to approve or reject user-submitted facts.

Maintain quality and relevance of facts.

--**Advanced Filtering & Search**

Search facts by keywords, categories, or popularity.

Sort facts by newest, oldest, or most favorited.

--**Random Fact Notifications**

Implement daily or weekly email notifications or push notifications with fun facts.

--**Gamification**

Introduce points, badges, or levels for users submitting or favoriting facts.

Encourage community engagement.

--**Multi-language Support**

Translate facts into different languages to reach a wider audience.

--**Fact Sharing**

Allow users to share facts on social media or generate shareable images/cards.

--**Integration with External APIs**

Fetch new facts automatically from public trivia APIs.

Keep the content fresh without manual updates.

--**Analytics & Insights**

Track most popular categories, most favorited facts, and active users.

Use insights to improve user experience and engagement.

--**Mobile-Friendly Design**

Optimize UI for mobile devices using responsive design.

Optionally, develop a mobile app version using frameworks like Streamlit for mobile or React Native.

## Support

If you encounter any issues or have any questions:
---Phone no. :9177485045
---Email ID: tejaswininaiduthota03@gmail.com
