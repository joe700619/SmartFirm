// Helper function to show alert in modal
function showAlert(elementId, message, type = 'danger') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.getElementById(elementId).innerHTML = alertHtml;
    document.getElementById(elementId).scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
