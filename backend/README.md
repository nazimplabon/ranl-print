# RANL PRINT Backend

This is a Django API + Admin backend. It does **not** render the public website; the frontend is a separate folder.

## Windows setup
```bat
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py createsuperuser
py manage.py runserver 8000
```

## URLs
- Admin: http://127.0.0.1:8000/admin/
- Products API: http://127.0.0.1:8000/api/catalog/products/
- Legacy price endpoint returns a no-price message only; quote requests are submitted through /api/quotes/create/.
- Quote API: http://127.0.0.1:8000/api/quotes/create/
- CSRF API: http://127.0.0.1:8000/api/csrf/

## Admin workflow
1. Create a superuser.
2. Open `/admin/`.
3. Edit Products.
4. Add Size, Paper/GSM, Printing, Finishing and Quantity Price rules using the inline tables.
5. Quote requests appear under Quotes.

## PostgreSQL
Set `DATABASE_URL` in `.env` when you are ready for PostgreSQL.

## Orders workflow
Approved quotes can be converted from the Quote admin list into Orders. Each order tracks customer, production status, payment status, paid/due amounts, delivery status, due date and tracking number.


## Staff roles (Phase 5)
Run:

```bash
python manage.py setup_roles
```

Then open **Django Admin → Users**, create staff accounts and assign one or more groups:

- **Owner** — full access
- **Manager** — day-to-day operations, catalog, quotes, orders, production and limited finance
- **Designer** — catalog, quotes, customer/order viewing
- **Production** — production workflow and order updates
- **Accounts** — payments, expenses, finance and order updates
- **Delivery** — delivery/order updates and production visibility

Django's model permissions enforce the role boundaries in Admin and the protected business APIs.


## Customer order tracking
- Public tracking API: `POST /api/orders/track/`
- Public tracking page: `/track/`
- Matching requires both the order number and the phone number saved on the order.

## Owner login recovery

From `backend` run:

```bat
python manage.py create_owner --username nazim9655
```

If that custom command is unavailable, use Django's built-in command:

```bat
python manage.py createsuperuser --username nazim9655
```

If the user already exists and you only need to reset the password:

```bat
python manage.py shell
```

Then:

```python
from django.contrib.auth import get_user_model
u = get_user_model().objects.get(username='nazim9655')
u.set_password('YOUR_NEW_PASSWORD')
u.is_active = True
u.is_staff = True
u.is_superuser = True
u.save()
exit()
```

Do not commit the password to source control.


## Pricing source of truth
The Django Admin catalog is the single source of truth for customer quote pricing. Product, size, paper/GSM, printing, finishing, and quantity-price changes are read live from the database by the Django-served website. The customer quote no longer uses hard-coded fallback/demo pricing.
