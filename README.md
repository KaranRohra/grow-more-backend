# Backend Setup

## Follow below steps

- Clone project using `https://github.com/KaranRohra/grow-more-backend`
- Create .env file at `backend/backend/.env`
- Message `@KaranRohra` for .env file content
- Go to project location using terminal
- And finally run this commands
  - `pip install -r requirements.txt`
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - `python manage.py runserver`

Note: Project will not run if `.env` file is not configure properly. It is recommended to use virtual env. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. You can install virtualenv using pip.
