# SmartFirm Project Architecture

## 1. Project Overview
**SmartFirm** is a Django-based enterprise application designed for firm management. The frontend utilizes **AdminLTE v4** (Bootstrap 5) to provide a responsive and professional user interface.

## 2. Agent Roles
To maintain project integrity and efficient development, we employ a multi-agent strategy:

### 🏛️ Architect Agent (Current Role)
- **Responsibility**: Overall system architecture, project structure maintenance, and cross-cutting concerns.
- **Scope**:
  - adding new "apps" or modules.
  - Making global configuration changes.
  - Ensuring adherence to design patterns.
  - Maintaining this `ARCHITECTURE.md` file.

### 🔨 Feature Agents (Future Roles)
- **Responsibility**: Implementing specific business logic within existing modules.
- **Scope**:
  - Example: "Registration Case Agent" for handling specific registration workflows.
  - These agents typically work within a specific app (e.g., `registration`, `hr`) and follow the patterns established by the Architect.

**⚠️ CRITICAL RULE**: Every Agent starting a new session MUST read this `ARCHITECTURE.md` file as their first step to understand the ground rules.

## 3. Directory Structure
The project follows a standard Django modular structure:

- **`smartfirm_project/`**: Project configuration root (`settings.py`, `urls.py`).
- **`admin_module/`**: Core administrative functionality (Customers, Contacts).
- **`registration/`**: Business logic for firm registration cases, shareholders, and vectors.
- **`hr/`**: Human Resources module.
- **`booking/`**: Booking and scheduling logic.
- **`templates/`**: Global templates (overrides) and base layouts.
- **`static/`**: Static assets (CSS, JS, Images).
- **`.agent/`**: Agent-specific configurations, skills, and workflows.

## 4. Architecture Standards

### 4.1 Technology Stack
- **Backend**: Django (Python)
- **Frontend Framework**: AdminLTE v4 (Bootstrap 5 based)
- **Icons**: Bootstrap Icons (`bi bi-*`)
- **Forms**: Django Forms / ModelForms with Bootstrap styling.

### 4.2 UI/UX Guidelines (Summary)
*For full details, refer to `.agent/skills/smartfirm_ui_standard/SKILL.md`*

- **List Views**: MUST use the AdminLTE **Card Pattern**.
  - `card-header` for title and actions.
  - `card-body` (p-0) for the table.
  - `table-striped table-hover` for data tables.
- **Action Buttons**:
  - **Edit**: Yellow (`btn-warning`)
  - **Delete**: Red (`btn-danger`)
  - **Add**: Primary (`btn-primary`) with icon.
- **Forms**: Standard Bootstrap form controls (`form-control`, `form-label`).

### 4.3 Development Workflow (Summary)
*For full details, refer to `.agent/skills/new_feature_workflow/SKILL.md`*

1.  **Models**: Define in `models.py`. **Run migrations immediately** after changes.
2.  **Forms**: Use `ModelForm` where possible.
3.  **Views**: Prefer Class-Based Views (ListView, CreateView, UpdateView).
4.  **Templates**: Extend `base.html`. Use Django template tags.
5.  **URLs**: Register usage of logical path names.
6.  **Navigation**: Update sidebar if a new top-level feature is added.

### 4.4 Coding Conventions
- **Naming**: Snake_case for Python variables/functions; CamelCase for Classes.
- **JavaScript**:
  - Avoid inline scripts in HTML when possible.
  - Use external JS files or `{% block extra_js %}`.
  - **Number Formatting**: Always use thousand separators for display (e.g., `1,000`).

## 5. Deployment & Environment
- **Local Dev**: `python manage.py runserver`
- **Settings**: strictly separated in `.env` file for sensitive keys.
