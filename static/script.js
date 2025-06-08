// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const resultsDropdown = document.getElementById('resultsDropdown');
    let debounceTimeout;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value;
        clearTimeout(debounceTimeout);

        if (query.length < 3) {
            resultsDropdown.innerHTML = '';
            resultsDropdown.classList.remove('show');
            return;
        }

        debounceTimeout = setTimeout(() => {
            fetchProducts(query);
        }, 300);
    });

    async function fetchProducts(query) {
        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const products = await response.json();
            displayResults(products);
        } catch (error) {
            console.error('Error fetching products:', error);
            resultsDropdown.innerHTML = '<div class="dropdown-item">Failed to fetch results.</div>';
            resultsDropdown.classList.add('show');
        }
    }

    function displayResults(products) {
        resultsDropdown.innerHTML = '';

        if (products.length === 0) {
            resultsDropdown.innerHTML = '<div class="dropdown-item">No results found.</div>';
        } else {
            products.forEach(product => {
                const linkElement = document.createElement('a');
                linkElement.className = 'dropdown-item';
                linkElement.href = product.product_url; // Set the link destination
                linkElement.target = "_blank"; // Open link in a new tab
                linkElement.rel = "noopener noreferrer"; // Security best practice

                // Construct the inner HTML for the link
                linkElement.innerHTML = `
                    <img src="${product.photo_url}" alt="${product.item}">
                    <div class="item-details">
                        <p class="item-name">${product.item}</p>
                        <p class="item-price">${product.price}</p>
                    </div>
                `;
                resultsDropdown.appendChild(linkElement);
            });
        }
        
        resultsDropdown.classList.add('show');
    }

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            resultsDropdown.classList.remove('show');
        }
    });
});