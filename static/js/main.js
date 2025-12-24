// Main JavaScript for Warehouse Management System

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm delete actions
    $('.btn-danger[data-confirm]').click(function(e) {
        if (!confirm($(this).data('confirm'))) {
            e.preventDefault();
        }
    });

    // Product search with debounce
    let searchTimeout;
    $('#search').on('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            // Auto-submit search form after 500ms of no typing
            // Uncomment if you want auto-search
            // $('#search').closest('form').submit();
        }, 500);
    });

    // Dynamic form handling for purchase orders
    if ($('.formset').length) {
        initializeFormset();
    }

    // Stock movement form enhancements
    if ($('#id_product').length) {
        $('#id_product').change(function() {
            const productId = $(this).val();
            if (productId) {
                loadProductInfo(productId);
            }
        });
    }

    // Number formatting
    $('.currency').each(function() {
        const value = parseFloat($(this).text());
        if (!isNaN(value)) {
            $(this).text('$' + value.toFixed(2));
        }
    });
});

// Load product information via AJAX
function loadProductInfo(productId) {
    $.ajax({
        url: `/api/product/${productId}/`,
        method: 'GET',
        success: function(data) {
            // Update unit price if field exists
            if ($('#id_unit_price').length) {
                $('#id_unit_price').val(data.unit_price);
            }
            
            // Show current stock info
            if ($('#current-stock-info').length) {
                $('#current-stock-info').html(`
                    <div class="alert alert-info">
                        <strong>${data.name}</strong> (${data.sku})<br>
                        Current Stock: <span class="badge bg-primary">${data.current_stock}</span>
                    </div>
                `);
            }
        },
        error: function() {
            console.log('Error loading product information');
        }
    });
}

// Initialize formset for purchase orders
function initializeFormset() {
    let formCount = parseInt($('#id_items-TOTAL_FORMS').val());
    
    // Add new form button
    $('#add-form').click(function(e) {
        e.preventDefault();
        
        const formTemplate = $('#empty-form').html();
        const newForm = formTemplate.replace(/__prefix__/g, formCount);
        
        $('#formset-container').append(newForm);
        formCount++;
        $('#id_items-TOTAL_FORMS').val(formCount);
        
        // Initialize new form
        initializeNewForm(formCount - 1);
    });
    
    // Remove form button
    $(document).on('click', '.remove-form', function(e) {
        e.preventDefault();
        $(this).closest('.formset-form').remove();
        updateFormIndices();
    });
}

// Initialize new form in formset
function initializeNewForm(index) {
    const form = $(`.formset-form:eq(${index})`);
    
    // Add product change handler
    form.find('select[name$="-product"]').change(function() {
        const productId = $(this).val();
        if (productId) {
            const unitPriceField = form.find('input[name$="-unit_price"]');
            loadProductInfoForForm(productId, unitPriceField);
        }
    });
}

// Load product info for specific form
function loadProductInfoForForm(productId, unitPriceField) {
    $.ajax({
        url: `/api/product/${productId}/`,
        method: 'GET',
        success: function(data) {
            unitPriceField.val(data.unit_price);
        },
        error: function() {
            console.log('Error loading product information');
        }
    });
}

// Update form indices after removal
function updateFormIndices() {
    $('.formset-form').each(function(index) {
        $(this).find('input, select, textarea').each(function() {
            const name = $(this).attr('name');
            if (name) {
                const newName = name.replace(/items-\d+-/, `items-${index}-`);
                $(this).attr('name', newName);
            }
            
            const id = $(this).attr('id');
            if (id) {
                const newId = id.replace(/id_items-\d+-/, `id_items-${index}-`);
                $(this).attr('id', newId);
            }
        });
        
        $(this).find('label').each(function() {
            const forAttr = $(this).attr('for');
            if (forAttr) {
                const newFor = forAttr.replace(/id_items-\d+-/, `id_items-${index}-`);
                $(this).attr('for', newFor);
            }
        });
    });
    
    $('#id_items-TOTAL_FORMS').val($('.formset-form').length);
}

// Utility functions
function showLoading(element) {
    element.html('<span class="spinner-border spinner-border-sm" role="status"></span> Loading...');
    element.prop('disabled', true);
}

function hideLoading(element, originalText) {
    element.html(originalText);
    element.prop('disabled', false);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Print function
function printPage() {
    window.print();
}

// Export to CSV (basic implementation)
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const cols = row.querySelectorAll('td, th');
        let csvRow = [];
        
        for (let j = 0; j < cols.length; j++) {
            csvRow.push('"' + cols[j].innerText.replace(/"/g, '""') + '"');
        }
        
        csv.push(csvRow.join(','));
    }
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'export.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}
