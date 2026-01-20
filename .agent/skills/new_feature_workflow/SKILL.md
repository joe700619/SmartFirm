---
name: New Feature Workflow
description: A comprehensive guide for adding new features to the SmartFirm Django project, ensuring consistency across models, views, templates, and URLs.
---

# New Feature Workflow

This skill guides you through the process of adding a new feature to the SmartFirm Django project. Follow these steps to ensure all components are correctly integrated and adhere to the project's structure.

## 1. Plan the Feature
Before writing code, understand the requirements:
- **Data Models**: What data needs to be stored? (e.g., New tables, fields)
- **Views**: What logic is required? (e.g., List view, Create view, Update view)
- **Templates**: What screens does the user see?
- **URLs**: What are the access paths?

## 2. Models (`models.py`)
- Define your models in the appropriate app (e.g., `admin_module`, `booking`, `registration`).
- Use descriptive field names.
- **IMPORTANT**: After creating models, always run:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## 3. Forms (`forms.py`)
- If the feature involves user input, create a `ModelForm` in `forms.py`.
- Use `Bootstrap` classes for styling (e.g., `form-control`) if custom rendering is needed, or rely on `crispy-forms` if configured.

## 4. Views (`views.py`)
- Prefer **Class-Based Views (CBVs)** (e.g., `ListView`, `CreateView`, `UpdateView`) for standard CRUD operations.
- Ensure proper permissions (e.g., `LoginRequiredMixin`) are applied.
- Pass necessary context data to templates.

## 5. Templates (`templates/`)
- Create HTML files in the app's template directory (e.g., `registration/templates/shareholders/`).
- Extend the base template: `{% extends 'base.html' %}`.
- Use Django template tags for dynamic content.
- Ensure the UI is consistent with the existing theme (Bootstrap).

## 6. URLs (`urls.py`)
- Register your views in the app's `urls.py`.
- Use logical path names (e.g., `path('transactions/add/', TransactionCreateView.as_view(), name='transaction_add')`).

## 7. Sidebar/Navigation
- If the new feature requires a menu item, update `templates/includes/sidebar.html` (or equivalent) to include the new link.

## 8. Verification
- Start the server: `python manage.py runserver`
- Navigate to the new URL.
- Test the functionality (Create, Read, Update, Delete).
- Check for any console errors.
