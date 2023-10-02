document.addEventListener('DOMContentLoaded', function() {
    // Check if the current page is the expense_insights.html page
    if (document.querySelector('.monthly-container')) {
        initExpenseInsights();
    }
    // Add more initializations for other pages as needed
});

function initExpenseInsights() {
    console.log('initExpenseInsights called');
    // Update the class name to match your HTML
    document.querySelectorAll('.edit-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const container = btn.closest('.monthly-container');
            
            // Toggle the editable fields and buttons
            toggleEdit(container);  // Ensure this function name matches your definition
        });
    });

    document.querySelectorAll('.delete-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('delete-entry-btn clicked');  // Add this line
            const row = btn.closest('.entry-row');

            console.log(row);
            
            // Handle entry removal
            handleRemoveEntry(row, true);  // For a recurring charge
            handleRemoveEntry(row, false);  // For a regular expense;
        });
    });
}

function toggleEdit(container) {
    const rows = container.querySelectorAll('.entry-row');
    const isEditing = container.getAttribute('data-is-editing') === 'true';
    
    // Toggle contenteditable attribute for each entry
    rows.forEach(row => {
        row.querySelectorAll('td:not(.delete-entry)').forEach(cell => {
            cell.setAttribute('contenteditable', isEditing ? "false" : "true");
        });
        
        // Show/hide delete button for each row
        const deleteButton = row.querySelector('.delete-entry');
        deleteButton.style.display = isEditing ? 'none' : 'table-cell';
    });
    
    // Toggle button text
    const editButton = container.querySelector('.edit-entry-btn');
    editButton.textContent = isEditing ? 'Edit Entries' : 'Apply';
    
    // Update the data-is-editing attribute
    container.setAttribute('data-is-editing', isEditing ? "false" : "true");
}

function handleRemoveEntry(row, isRecurring) {
    const entryId = row.getAttribute('data-entry-id');
    console.log(entryId);
    
    fetch('/remove-entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: entryId, isRecurring: isRecurring })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            row.remove();  // Remove the entry from the table
        } else {
            alert('Error removing entry.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// This function should be called from the appropriate places
function toggleRemoveButtonVisibility(row, isEditing) {
    const removeButtonContainer = row.querySelector('.remove-container');
    if (isEditing) {
        removeButtonContainer.style.display = 'flex'; // Use 'flex' to maintain the centering of the "x"
        removeButtonContainer.addEventListener('click', handleRemoveEntry);
    } else {
        removeButtonContainer.style.display = 'none';
        removeButtonContainer.removeEventListener('click', handleRemoveEntry);
    }
}
