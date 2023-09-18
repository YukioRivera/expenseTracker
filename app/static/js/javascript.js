document.addEventListener('DOMContentLoaded', function() {
    // Check if the current page is the expense_insights.html page
    if (document.querySelector('.monthly-container')) {
        initExpenseInsights();
    }
    // Add more initializations for other pages as needed
});

function initExpenseInsights() {
    document.querySelectorAll('.edit-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('.entry-row');
            
            // Make the fields editable
            row.querySelector('.entry-date').contentEditable = true;
            row.querySelector('.entry-time').contentEditable = true;
            row.querySelector('.entry-category').contentEditable = true;
            row.querySelector('.entry-amount').contentEditable = true;
            
            // Hide the edit button and show the apply button
            btn.style.display = 'none';
            row.querySelector('.apply-entry-btn').style.display = 'block';
        });
    });

    document.querySelectorAll('.apply-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('.entry-row');
            
            // Extract the edited data
            const date = row.querySelector('.entry-date').textContent;
            const time = row.querySelector('.entry-time').textContent;
            const category = row.querySelector('.entry-category').textContent;
            const amount = row.querySelector('.entry-amount').textContent;
            
            // TODO: Send the updated data to the backend using AJAX
            
            // Make the fields non-editable again
            row.querySelector('.entry-date').contentEditable = false;
            row.querySelector('.entry-time').contentEditable = false;
            row.querySelector('.entry-category').contentEditable = false;
            row.querySelector('.entry-amount').contentEditable = false;
            
            // Hide the apply button and show the edit button
            btn.style.display = 'none';
            row.querySelector('.edit-entry-btn').style.display = 'block';
        });
    });
}

// Add more functions for other pages as needed
