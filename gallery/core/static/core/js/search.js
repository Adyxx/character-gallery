

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('global-search-form');
    const searchInput = document.getElementById('global-search');
    const resultsContainer = document.getElementById('search-results');

    if (!searchForm || !searchInput || !resultsContainer) {
        return;
    }

    let requestController = null;
    let debounceTimer = null;

    const hideResults = () => {
        resultsContainer.style.display = 'none';
        resultsContainer.innerHTML = '';
    };

    const showResults = () => {
        resultsContainer.style.display = 'grid';
    };

    const renderResults = (items) => {
        if (items.length === 0) {
            resultsContainer.innerHTML = '<div class="search-item muted">No pages found</div>';
            showResults();
            return;
        }

        resultsContainer.innerHTML = items.map((item) => `
            <a href="${item.url}" class="search-item">
                <div class="search-item-info">
                    <span class="search-item-title">${item.title}</span>
                    <span class="search-item-badge">${item.subtitle}</span>
                </div>
            </a>
        `).join('');
        showResults();
    };

    const runSearch = async () => {
        const query = searchInput.value.trim();
        
        /*if (query.length < 2) {
            if (requestController) {
                requestController.abort();
                requestController = null;
            }
            hideResults();
            return;
        }*/
        
        if (requestController) {
            requestController.abort();
        }

        requestController = new AbortController();

        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`, {
                signal: requestController.signal,
            });

            if (!response.ok) {
                throw new Error('Search request failed');
            }

            const data = await response.json();
            renderResults(Array.isArray(data.results) ? data.results : []);
            requestController = null;
        } catch (error) {
            if (error.name === 'AbortError') {
                return;
            }

            resultsContainer.innerHTML = '<div class="search-item muted">Search temporarily unavailable</div>';
            showResults();
            requestController = null;
        }
    };

    searchInput.addEventListener('input', () => {
        window.clearTimeout(debounceTimer);
        if (searchInput.value.trim().length < 2 && requestController) {
            requestController.abort();
            requestController = null;
        }
        debounceTimer = window.setTimeout(runSearch, 180);
    });

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        runSearch();
    });

    document.addEventListener('click', (event) => {
        if (!searchForm.contains(event.target) && !resultsContainer.contains(event.target)) {
            hideResults();
        }
    });
});