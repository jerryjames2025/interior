// Live Search Implementation
function initializeSearch(searchType) {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchLoading = document.querySelector('.search-loading');
    let searchTimeout;

    if (!searchInput || !searchResults) {
        console.error('Search elements not found');
        return;
    }

    // Create loading spinner if it doesn't exist
    if (!searchLoading) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'search-loading';
        loadingDiv.innerHTML = '<div class="spinner"></div>';
        searchInput.parentNode.appendChild(loadingDiv);
    }

    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        // Hide results if query is empty
        if (query.length < 2) {
            searchResults.style.display = 'none';
            if (searchLoading) searchLoading.style.display = 'none';
            return;
        }
        
        // Show loading spinner
        if (searchLoading) searchLoading.style.display = 'block';
        
        // Set a timeout to prevent too many requests
        searchTimeout = setTimeout(() => {
            // Determine the search endpoint based on the type
            const endpoint = searchType === 'designs' ? '/search-designs/' : '/search-products/';
            
            fetch(`${endpoint}?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (searchLoading) searchLoading.style.display = 'none';
                
                if (data.success) {
                    // Clear previous results
                    searchResults.innerHTML = '';
                    
                    if (data.results.length > 0) {
                        data.results.forEach(result => {
                            const resultItem = document.createElement('div');
                            resultItem.className = 'search-result-item';
                            
                            // Different HTML structure for designs vs products
                            if (searchType === 'designs') {
                                resultItem.innerHTML = `
                                    <a href="/design-detail/${result.id}/" class="search-result-link">
                                        <div class="search-result-image">
                                            ${result.image ? `<img src="${result.image}" alt="${result.name}">` : ''}
                                        </div>
                                        <div class="search-result-info">
                                            <div class="search-result-title">${result.name}</div>
                                            <div class="search-result-category">${result.category}</div>
                                            <div class="search-result-description">${result.description}</div>
                                        </div>
                                    </a>
                                `;
                            } else {
                                resultItem.innerHTML = `
                                    <a href="/product-detail/${result.id}/" class="search-result-link">
                                        <div class="search-result-image">
                                            ${result.image ? `<img src="${result.image}" alt="${result.name}">` : ''}
                                        </div>
                                        <div class="search-result-info">
                                            <div class="search-result-title">${result.name}</div>
                                            <div class="search-result-category">${result.category}</div>
                                            <div class="search-result-description">${result.description}</div>
                                            <div class="search-result-price">₹${result.price}</div>
                                        </div>
                                    </a>
                                `;
                            }
                            searchResults.appendChild(resultItem);
                        });
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div class="search-result-item no-results">No results found</div>';
                        searchResults.style.display = 'block';
                    }
                } else {
                    searchResults.innerHTML = '<div class="search-result-item error-message">Error performing search</div>';
                    searchResults.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Search error:', error);
                if (searchLoading) searchLoading.style.display = 'none';
                searchResults.innerHTML = '<div class="search-result-item error-message">Error performing search</div>';
                searchResults.style.display = 'block';
            });
        }, 300);
    });

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (searchResults && !searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.style.display = 'none';
        }
    });

    // Keep the original search button functionality for fallback
    const searchButton = document.getElementById('searchButton');
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            const query = searchInput.value;
            if (query) {
                // Redirect to the search page with the query
                const searchPage = searchType === 'designs' ? '/designs/' : '/products/';
                window.location.href = `${searchPage}?search=${encodeURIComponent(query)}`;
            }
        });

        // Support Enter key for search
        searchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                searchButton.click();
            }
        });
    }
} 