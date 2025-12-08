# DEC-Launchpad-ZenQuotes API Python Project

An automated platform for delivering daily inspirational quotes to subscribed users. This system fetches quotes from the ZenQuotes API, stores them in a PostgreSQL database, and sends personalized emails based on user preferences.

The MindFuel Mental Wellness Startup system automatically delivers inspirational quotes to subscribers. It pulls daily quotes from the ZenQuotes API, stores them in a database, and sends personalized emails at 7:00 AM based on user frequency preferences (daily or weekly).

## System Architecture

![alt text](images/Architectural%20diagram.png)

## Key Features

✅ Automated Quote Fetching: Daily retrieval from ZenQuotes API with retry logic

✅ Personalized Email Delivery: Customized quotes sent to users based on preferences

✅ Comprehensive Logging: Application and database tracking for monitoring

✅ Scalable Architecture: Designed to support hundreds to thousands of users

✅ Admin Reporting: Daily summary emails with delivery statistics

## Technical Implementation
### Database Schema

The PostgreSQL database includes three main tables:

💠zenquote: Stores daily quotes with timestamps

💠 users: Manages subscriber information and preferences

💠 email_log: Tracks all email delivery attempts

See [the sql statement](SQLstatement.sql) for complete schema definition.

### Core Functions Implemented

| Function                    | Purpose                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`get_daily_quote()`**     | Fetches a new quote from ZenQuotes API. Includes 2 retries in case of network failure and logs each attempt.                                                             |
| **`save_quote_to_db()`**    | Inserts the fetched quote and author into the `zenquote` table in the database.                                                                                          |
| **`get_users()`**           | Retrieves active users from the `users` table based on their email frequency preference (daily or weekly). Returns firstname and email for each user.                    |
| **`send_email()`**          | Sends emails using Gmail SMTP. Uses an *App Password* (generated in Gmail under **Manage Account → App Passwords**) for security instead of the main password.           |
| **`log_email_status()`**    | Records both successful and failed email sends into the `email_log` table for traceability and monitoring.                                                               |
| **`send_summary_report()`** | Sends a summary report to the admin email (set in `.env`) detailing how many emails were sent successfully or failed. Missing this report indicates a scheduler failure. |

### Email Configuration

💠 During testing, Gmail’s default SMTP on port 587 (STARTTLS) failed due to timeout or firewall issues. Switching to SSL (port 465) resolved the problem, and email sending worked correctly.

💠 Implements App Passwords for enhanced security

💠 Supports personalized content based on user preferences

### Logging & Monitoring

**Application logs** are saved in [quotes_mailer.log](quotes_mailer.log), showing daily activities, retries, and email status.

**Database logs** are stored in the email_log table, including email address, firstname, frequency, quote, author, send status, and timestamp. This provides complete visibility for monitoring and analytics.

**Admin Reports:** Daily summary emails with success/failure metrics.

### Scheduling (Windows Task Scheduler)

The system is configured to run automatically:

-- Daily at 7:00 AM for daily subscribers

-- Weekly at 7:00 AM for weekly subscribers

Setup steps:

1. Create new task with appropriate name and description

2. Set trigger for daily/weekly execution at 7:00 AM

3. Configure action to run Python script with required arguments

4. Test configuration to ensure proper execution


## Installation & Setup
### Prerequisites
1. Python 3.8+

2. PostgreSQL

3. Gmail account with App Password configured

**Configuration**

1. Clone the repository

2. Install dependencies: pip install -r requirements.txt

3. Set up PostgreSQL database using [the sql statement](SQLstatement.sql)

4. Configure environment variables in `.env` file

5. Generate Gmail App Password for secure email sending

**Environment Variables**

    DATABASE_URL=postgresql://user:password@localhost/dbname
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=465
    EMAIL_USER=your-email@gmail.com
    EMAIL_PASSWORD=your-app-password
    ADMIN_EMAIL=admin@example.com

**Alternative Scheduling**

For cross-platform deployment, consider:

1. Cron jobs (Linux/Mac) or

2. Docker containers with scheduled execution or

3. Cloud-based scheduler services