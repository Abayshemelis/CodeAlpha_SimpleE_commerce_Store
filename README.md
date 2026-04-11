# EthioE_commerce_SimpleE_com  

**EthioE_commerce_SimpleE_com** is a simple Django-based e-commerce web app designed to demonstrate product listing, details pages, a shopping cart, and a checkout flow.  It uses plain Django templates for the frontend (in a `FrontendTemplate/` folder) and manages static assets (CSS/JS/images) under a `static/` directory.  The project is structured into three Django apps: `store` (products), `orders` (cart & checkout), and `users` (authentication). The default database is SQLite for quick development, but PostgreSQL is fully supported and **optional** for production use (with [psycopg2](https://www.psycopg.org/) or `psycopg3` as the adapter)【18†L135-L138】【2†L179-L181】.  

**Key Features:** 

- **Product Catalog:** List products with name, price, description, and image.  
- **Product Detail Page:** View full details of each product.  
- **Shopping Cart:** Add/remove items and view cart contents.  
- **Checkout Workflow:** Create an order from the cart.  
- **User Accounts:** User registration and login (via the `users` app).  
- **Admin Interface:** Manage products and orders through Django’s admin.  

## Tech Stack  
- **Backend:** Django (3.2+ or latest 4.x) with Python (recommended 3.11 or 3.12).  *Newer Python versions (3.13+) on Windows may lack pre-built `psycopg2` wheels; downgrade to 3.12 if needed*【24†L208-L214】.  
- **Database:** PostgreSQL (14+) recommended for production; SQLite (`db.sqlite3`) is default for development.  *If using Postgres, install `psycopg2-binary` or `psycopg3`*【18†L135-L138】【2†L179-L181】.  
- **Frontend:** Django templates (in `FrontendTemplate/`), HTML5, CSS, and JavaScript. Static files (CSS, JS, images) are served from the `static/` folder. Templates load static assets via Django’s `{% static %}` tag【21†L82-L90】.  
- **Libraries:** [Pillow](https://pillow.readthedocs.io/) for image handling, (optionally) `python-decouple` or `django-environ` for environment config, and `gunicorn` for production WSGI server.  

## Project Structure  
```
CodeAlpha_SimpleE_com/
├─ manage.py
├─ db.sqlite3               # (SQLite DB, or remove if using only Postgres)
├─ ecommerce/               # Django project config
│   ├─ settings.py
│   └─ urls.py
├─ FrontendTemplate/        # HTML templates (frontend)
│   ├─ base.html
    ├─ cart_summary.html
    ├─ checkout.html
│   ├─ home.html
    ├─ contact.html
│   └─ product_detail.html
├─ static/                  # Static assets
│   ├─ css/
│   │   └─ style.css
│   ├─ js/
    ├   └─script.js
├─ store/                   # App: product catalog
│   ├─ models.py
│   ├─ admin.py
│   ├─ views.py
│   ├─ urls.py  
│   ├─cart.py


├─ orders/                  # App: cart & orders
│   ├─ models.py
│   └─ views.py
└─ users/                   # App: user auth (optional)
    ├─ models.py
    └─ views.py
```
Each app has its own URL config (e.g. `store/urls.py`) included in `ecommerce/urls.py`. 

## Installation

### Prerequisites
- **Python 3.11+** installed.  (See [Python’s venv docs](https://docs.python.org/3/library/venv.html) – Django recommends using a virtual environment【16†L200-L207】.)  
- **pip** (Python package manager) up to date.  
- **PostgreSQL** server if you plan to use it (optional; [download from postgresql.org](https://www.postgresql.org/download/)).  
- (Optional) `virtualenv`/`venv` tool for creating isolated environments.  

### Setup Steps
1. **Clone the repository:** (replace `<REPO_URL>` with the actual Git repo URL)  
   ```bash
   git clone <REPO_URL>
   cd CodeAlpha_SimpleE_com
   ```  
2. **Create and activate a virtual environment:**  
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```  
   This ensures dependencies are isolated【16†L200-L207】.  

3. **Install Python dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```  
   This will install Django, `psycopg2-binary` (if using Postgres), Pillow, etc.  

4. **Configure the database:**  
   - *Using PostgreSQL:* Create a database and user (for example, using `psql`):  
     ```sql
     CREATE DATABASE ecommerce_db;
     CREATE USER myuser WITH PASSWORD 'password';
     GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO myuser;
     ```  
     Then update `ecommerce/settings.py` (or your `.env`/`docker-compose` file) with your Postgres credentials, e.g.:  
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'ecommerce_db',
             'USER': 'myuser',
             'PASSWORD': 'password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```  
     Django’s docs note that after creating the database and user, you must run migrations to create tables【18†L171-L174】.
   - *Using SQLite (default):* No setup needed. The default `DATABASES` uses `BASE_DIR / 'db.sqlite3'`.  

5. **Set environment variables:** Create a `.env` file or export as needed. For example:  
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgres://myuser:password@localhost:5432/ecommerce_db
   ```  
   (Adjust settings.py to read these, e.g. via `python-decouple` or `django-environ`.)  

6. **Run database migrations:**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```  
   This creates tables for the `store`, `orders`, `users`, and built-in auth apps.  

7. **Create an admin user:**  
   ```bash
   python manage.py createsuperuser
   ```  

8. **Start the development server:**  
   ```bash
   python manage.py runserver
   ```  
   Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).  

## Usage

- **Django Admin:** Visit `/admin`, log in with your superuser, and add **Products** (fill name, price, description, and image). The `store/admin.py` registers the `Product` model.  
- **Home Page:** Visit `/` to see a list of products (template: `home.html`).  
- **Product Detail:** Click a product to view its details (e.g. `/product/1/` for ID=1, template: `product_detail.html`).  
- **Shopping Cart:** (If implemented) add items to cart and view at `/cart/`.  
- **Checkout:** Place an order at `/checkout/`.  
- **Sample URLs:**  
  - Home/Product listing: `http://localhost:8000/`  
  - Product page: `http://localhost:8000/product/1/`  
  - Admin panel: `http://localhost:8000/admin/`  

*(Replace `localhost:8000` with your domain/port as needed.)*  

## Development Notes

- **Switching DB to SQLite:** To revert to SQLite for development, set in `settings.py`:  
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / "db.sqlite3",
      }
  }
  ```  
  No external DB is needed (SQLite is file-based by default).  
- **Static & Media Files:**  
  - During development, with `DEBUG=True`, Django’s `runserver` will automatically serve static files (see Django docs【21†L98-L100】).  
  - For production, run `python manage.py collectstatic` to gather static files, and configure your web server (e.g. Nginx or Apache) to serve the `/static/` and `/media/` directories.  
- **Production Deployment:** Use a production WSGI server. For example, install Gunicorn and run:  
  ```bash
  pip install gunicorn
  gunicorn ecommerce.wsgi:application
  ```  
  This starts the app with Gunicorn (a pure-Python WSGI server)【11†L72-L81】. You may then place Nginx or Apache in front of Gunicorn to handle TLS, static files, etc. Official guides (e.g. on djangoproject.com or DigitalOcean) provide detailed deployment steps.  

## Code Snippets

**`store/models.py` (Product model):**  
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
```

**`store/admin.py` (register the model):**  
```python
from django.contrib import admin
from .models import Product

admin.site.register(Product)
```

**`store/urls.py`:**  
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]
```

**`ecommerce/urls.py`:**  
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]
```

**`FrontendTemplate/base.html`:**  
```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>My Django Shop</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <h1>My Store</h1>
    {% block content %}{% endblock %}
</body>
</html>
```

**`FrontendTemplate/home.html`:**  
```html
{% extends 'base.html' %}
{% block content %}
<h2>Products</h2>
<div class="products">
  {% for product in products %}
    <div class="card">
      <h3>{{ product.name }}</h3>
      <p>${{ product.price }}</p>
    </div>
  {% endfor %}
</div>
{% endblock %}
```
*(These examples show loading static CSS and using template inheritance. See Django’s staticfiles docs for more on `{% load static %}`【21†L82-L90】.)*  

## Development vs Production Settings

| Setting            | Development                | Production               |
|--------------------|----------------------------|--------------------------|
| `DEBUG`            | `True` (debug mode)        | `False`                  |
| `ALLOWED_HOSTS`    | `['localhost','127.0.0.1']`| e.g. `['example.com']`   |
| Database Engine    | SQLite (`db.sqlite3`)      | PostgreSQL              |
| Static Files       | Served by `runserver` (debug)【21†L98-L100】 | `collectstatic` + served by Nginx/Apache |
| WSGI Server        | Django dev server          | Gunicorn + webserver【11†L72-L81】 |

## Contributing

Contributions are welcome! Feel free to fork the repo and open a pull request. For major changes, open an issue first to discuss. Please follow PEP8 and Django coding standards, and include tests if applicable.

## License

This project is released under the **MIT License** – see [LICENSE](LICENSE) for details.  

*(Author and repository details are unspecified in this template; replace placeholders (e.g. `<REPO_URL>`) and add your name or project description as needed.)*  

### Example Request Flow Diagram

```mermaid
flowchart LR
    A[Home] --> B[Product Detail]
    B --> C[Cart]
    C --> D[Checkout]
```

## Example `requirements.txt`

```text
Django>=4.0,<5.0
psycopg2-binary>=2.9,<3.0
pillow>=9.0
python-decouple>=3.0
gunicorn
```