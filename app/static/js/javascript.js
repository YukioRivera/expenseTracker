document.addEventListener('DOMContentLoaded', function() {
    // Attach click event listeners to tabs to save the active tab's ID to localStorage
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            localStorage.setItem('activeTab', tab.id);
        });
    });

    // Check if the current page is the history.html page
    if (document.querySelector('.monthly-container')) {
        initExpenseHistory();
    }

    // Retrieve the active tab from localStorage and activate it
    const activeTabId = localStorage.getItem('activeTab');
    if (activeTabId) {
        const activeTab = document.getElementById(activeTabId);
        if (activeTab) {
            activeTab.click(); // This simulates a click on the tab, activating it.
        }
    }

    // Add more initializations for other pages as needed
});

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
        localStorage.setItem('activeTab', tab.id);
    });
});

function initExpenseHistory() {
    console.log('initExpenseHistory called');
    document.querySelectorAll('.edit-entry-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const container = btn.closest('.monthly-container');
            
            // Toggle the editable fields and buttons
            toggleEdit(container);

            const { regularEntries, recurringEntries, incomeEntries } = collectEditedEntries();
            console.log("this is to check income entries 1 "  + incomeEntries)
            
            if (regularEntries.length > 0) {
                updateEntries(regularEntries);
            }

            if (recurringEntries.length > 0) {
                updateRecurringEntries(recurringEntries);
            }

            if (incomeEntries.length > 0) {
                console.log("this is to check income entries 2 "  + incomeEntries)
                updateIncomeEntries(incomeEntries);
            }
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

    // Track edited rows for recurring expenses
    document.querySelectorAll('.recurring-entry-row').forEach(row => {
        row.addEventListener('input', function() {
            row.classList.add('edited-recurring-entry-row');
        });
    });
}


function toggleEdit(container) {
    // Determine the type of tab we're in
    const isInExpensesTab = container.querySelector('.expenses-table') !== null;
    const isInIncomeTab = container.querySelector('.income-table') !== null;

    // Get all rows inside the current container
    const rows = container.querySelectorAll('.entry-row');
    const isEditing = container.getAttribute('data-is-editing') === 'true';
    
    // Update the data-is-editing attribute first
    container.setAttribute('data-is-editing', isEditing ? "false" : "true");
    
    // Toggle contenteditable attribute for each entry
    rows.forEach(row => {
        row.querySelectorAll('td:not(.delete-entry):not(.edit-entry)').forEach(cell => {
            cell.setAttribute('contenteditable', isEditing ? "false" : "true");
        });
        
        // Show/hide delete button for each row
        const deleteButton = row.querySelector('.delete-entry');
        if (deleteButton) {
            deleteButton.style.display = isEditing ? 'none' : 'table-cell';
        }

        // Show/hide edit button for each row (specifically for Income)
        const editButton = row.querySelector('.edit-entry');
        if (editButton) {
            editButton.style.display = isEditing ? 'none' : 'table-cell';
        }
    });
    
    // Toggle button text
    const editButton = container.querySelector('.edit-entry-btn');
    editButton.textContent = isEditing ? 'Edit Entries' : 'Apply';
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
    const regularEntries = [];
    const recurringEntries = [];
    const incomeEntries = [];

    Array.from(editedEntryRows).forEach(row => {
        if (row.classList.contains('recurring-entry-row')) {
            // Handle recurring expenses
            recurringEntries.push({
                id: row.dataset.entryId,
                startDate: row.querySelector('.entry-date').value,
                endDate: row.querySelector('.entry-end-date').value || null,
                category: row.querySelector('.entry-category').textContent,
                amount: row.querySelector('.entry-amount').textContent
            });
        } else if (row.closest('.income-table')) {
            // Handle income
            incomeEntries.push({
                id: row.dataset.entryId,
                date: row.querySelector('.entry-date').value,
                source: row.querySelector('.entry-source').textContent,
                amount: row.querySelector('.entry-amount').textContent
            });
        } else {
            // Handle regular expenses
            regularEntries.push({
                id: row.dataset.entryId,
                date: row.querySelector('.entry-date').value,
                description: row.querySelector('.entry-description').textContent,
                category: row.querySelector('.entry-category').textContent,
                amount: row.querySelector('.entry-amount').textContent
            });
        }
    });

    console.log("Regular Entries:", regularEntries);
    console.log("Recurring Entries:", recurringEntries);
    console.log("Income Entries:", incomeEntries);

    return {
        regularEntries: regularEntries,
        recurringEntries: recurringEntries,
        incomeEntries: incomeEntries
    };
}

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

function updateRecurringEntries(entries) {
    fetch('/update-recurring-entries', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entries: entries }),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`Request failed with status ${response.status}: ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log('Recurring entries updated successfully');
        } else {
            console.error('Error updating recurring entries:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateIncomeEntries(entries) {
    fetch('/update-income-entries', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entries: entries }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Income entries updated successfully');
        } else {
            console.error('Error updating income entries:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

$(document).ready(function() {
    // Check for the saved tab in sessionStorage and activate it
    var activeTab = sessionStorage.getItem('activeTab');
    if (activeTab) {
        $('.nav-tabs a[href="' + activeTab + '"]').tab('show');
    }

    // Save the current tab to sessionStorage when clicked
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        sessionStorage.setItem('activeTab', $(e.target).attr('href'));
    });
});
