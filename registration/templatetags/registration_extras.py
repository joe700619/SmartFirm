from django import template

register = template.Library()

@register.filter
def comma_sep(value):
    """
    Format a number with comma thousand rendering.
    Usage: {{ value|comma_sep }}
    """
    try:
        if value is None:
            return ""
        # Handle float/decimal to preserve decimals if present?
        # User wants 1,000 and 10,000.00
        # Simple {:,} does this for floats and ints appropriately?
        # {:,.2f} forces 2 decimals. {:,} preserves default.
        # Let's check type.
        val = float(value)
        if val.is_integer():
             return f"{int(val):,}"
        return f"{val:,}"
    except (ValueError, TypeError):
        return value
