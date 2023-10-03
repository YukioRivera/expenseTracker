document.addEventListener('DOMContentLoaded', function() {
    // Check if the current page is the expense_insights.html page
    if (document.querySelector('.monthly-container')) {
        initExpenseInsights();
    }
    // Add more initializations for other pages as needed
});

function initExpenseInsights() {
    console.log('initExpenseInsights called');
    document.querySelectorAll('.edit-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const container = btn.closest('.monthly-container');
            
            // Toggle the editable fields and buttons
            toggleEdit(container);
        });
    });

    document.querySelectorAll('.delete-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('.entry-row');
            handleRemoveEntry(row, true);  // For a recurring charge
            handleRemoveEntry(row, false);  // For a regular expense;
        });
    });

    // Track edited rows
    document.querySelectorAll('.entry-row').forEach(row => {
        row.addEventListener('input', function() {
            row.classList.add('edited-entry-row');
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

function collectEditedEntries() {
    const editedEntryRows = document.querySelectorAll('.edited-entry-row');
    const editedEntries = Array.from(editedEntryRows).map(row => {
        return {
            id: row.dataset.entryId,
            date: row.querySelector('.entry-date').textContent,
            time: row.querySelector('.entry-time').textContent,
            category: row.querySelector('.entry-category').textContent,
            amount: row.querySelector('.entry-amount').textContent,
            endDate: row.querySelector('.entry-end-date') ? row.querySelector('.entry-end-date').textContent : null
        };
    });
    console.log("editedEntries:", editedEntries);
    return editedEntries;
}

document.querySelector('#edit-entries-btn').addEventListener('click', function() {
    const editedEntries = collectEditedEntries();
    updateEntries(editedEntries);
});

function updateEntries(entries) {
    fetch('/update-entries', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entries: entries }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Entries updated successfully');
        } else {
            console.error('Error updating entries:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
