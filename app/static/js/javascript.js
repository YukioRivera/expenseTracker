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
            toggleEditableFields(row, true);
            
            // Hide the edit button and show the apply button
            toggleEditApplyButtons(row, false);
        });
    });

    document.querySelectorAll('.apply-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('.entry-row');
            
            // Extract the edited data and send to server
            updateEntry(row);
            
            // Make the fields non-editable again
            toggleEditableFields(row, false);
            
            // Hide the apply button and show the edit button
            toggleEditApplyButtons(row, true);
        });
    });
}

function toggleEditableFields(row, isEditable) {
    row.querySelector('.entry-date').contentEditable = isEditable;
    row.querySelector('.entry-time').contentEditable = isEditable;
    row.querySelector('.entry-category').contentEditable = isEditable;
    row.querySelector('.entry-amount').contentEditable = isEditable;
}

function toggleEditApplyButtons(row, isEditVisible) {
    row.querySelector('.edit-entry-btn').style.display = isEditVisible ? 'block' : 'none';
    row.querySelector('.apply-entry-btn').style.display = isEditVisible ? 'none' : 'block';
}

function updateEntry(row) {
    const entryId = row.getAttribute('data-entry-id');
    const date = row.querySelector('.entry-date').textContent;
    const time = row.querySelector('.entry-time').textContent;
    const category = row.querySelector('.entry-category').textContent;
    const amount = row.querySelector('.entry-amount').textContent;
    
    fetch('/update-entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            entry_id: entryId,
            date: date,
            time: time,
            category: category,
            amount: amount
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Handle success message
        } else if (data.error) {
            // Handle error message
        }
    });
}

function handleRemoveEntry(event) {
    const row = event.target.closest('.entry-row');
    const entryId = row.getAttribute('data-entry-id');

    fetch('/remove-entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: entryId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            row.remove();  // Remove the entry from the table
        } else {
            alert('Error removing entry.');
        }
    });
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
