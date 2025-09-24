# Fun Fact Generator Web App

The Fun Fact Generator Web App is an interactive platform that delivers random, interesting, and educational facts to users. Unlike traditional console-based programs, this app provides a modern web interface where users can explore facts by categories such as Science, History, and Technology.This project combines frontend interactivity (Streamlit), backend API handling (FastAPI), and database management (Supabase) to create a fun, educational, and user-friendly web application.

## Features

_**Random Fact Generation**: Users can click a button to instantly receive a new fun fact.

_**Categorized Facts**: Facts are organized into categories, making it easier to explore topics of interest.

_**User Profiles and Favorites**: Users can save their favorite facts to their profile for easy access.

_**Community-driven Content**: Users can submit their own fun facts, allowing the database to grow dynamically.

_**Database Integration**: All facts, user data, and favorites are stored securely in a Supabase (PostgreSQL) database.

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
create table users (
    id uuid primary key default gen_random_uuid(),
    username text unique not null,
    email text unique not null,
    password_hash text not null,
    created_at timestamp default now()
);


create table fun_facts (
    id uuid primary key default gen_random_uuid(),
    category text not null,
    fact_text text not null,
    created_by uuid references users(id),
    created_at timestamp default now()
);


create table user_favorites (
    user_id uuid references users(id) on delete cascade,
    fact_id uuid references fun_facts(id) on delete cascade,
    primary key(user_id, fact_id),
    favorited_at timestamp default now()
);

```
3. **Get Your Credentials:

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

## Technical Details

### Technologies Used

_ **Frontend**: Streamlit (Python web framework)
_ **Backend**: FatsAPI  (Python REST API frameworks)
_ **Database**: Supabase (PostgreSQL-based backend-as-a-service)
_ **Language**: Python 3.8+

### Key Components

1. **`src/db.py`**: Database operations-Handles all CRUD operations with Supabase

2. **`src/logic.py`**: Business logic -Task validation and processing

## Troubleshooting

## Common Issues

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
