// Logic to render universities
const container = document.getElementById('rankings-container');
const mapContainer = document.getElementById('map-container');
const searchInput = document.getElementById('searchInput');
const favoritesBtn = document.createElement('button');
favoritesBtn.textContent = "❤️ Favorites";
favoritesBtn.className = "filter-btn";
favoritesBtn.id = "favoritesBtn";
document.querySelector('.filters').appendChild(favoritesBtn);
const filterBtns = document.querySelectorAll('.filter-btn');
const listViewBtn = document.getElementById('listViewBtn');
const mapViewBtn = document.getElementById('mapViewBtn');

// Comparator Elements
const compareFab = document.getElementById('compare-fab');
const compareCount = document.querySelector('.compare-count');
const compareModal = document.getElementById('compare-modal');
const compareGrid = document.getElementById('compare-grid');
const closeModal = document.querySelector('.close-modal');

let currentData = [...universities];
let map = null;
let markers = [];
let compareList = [];
let favorites = JSON.parse(localStorage.getItem('erasmusFavorites')) || [];
let showFavoritesOnly = false;

// Initialize Map
function initMap() {
    if (map) return; // Already initialized

    // Center on Europe approx
    map = L.map('map-container').setView([48.0, 15.0], 4);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
}

function updateMapMarkers(data) {
    if (!map) return;

    // Clear existing
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    data.forEach(uni => {
        if (uni.coords) {
            const marker = L.marker(uni.coords).addTo(map);
            marker.bindPopup(`
                <div style="color: #333; text-align: center;">
                    <strong style="font-size: 1.1em">${uni.name}</strong><br>
                    ${uni.city}, ${uni.country}<br>
                    <span style="font-size: 0.9em; color: #666;">📏 ${uni.distance_tul} km from TUL</span><br>
                    <span style="color: #00b894; font-weight: bold;">Score: ${uni.scores.total}</span>
                </div>
            `);
            markers.push(marker);
        }
    });
}

function toggleFavorite(uniName) {
    if (favorites.includes(uniName)) {
        favorites = favorites.filter(n => n !== uniName);
    } else {
        favorites.push(uniName);
    }
    localStorage.setItem('erasmusFavorites', JSON.stringify(favorites));
    renderCards(currentData); // Re-render to update hearts
}

function renderCards(data) {
    container.innerHTML = '';

    let displayData = data;
    if (showFavoritesOnly) {
        displayData = data.filter(uni => favorites.includes(uni.name));
        if (displayData.length === 0) {
            container.innerHTML = '<div style="text-align:center; grid-column: 1/-1; padding: 2rem;"><h3>No favorites yet! ❤️</h3><p>Click the heart icon on any card to add it here.</p></div>';
            return;
        }
    }

    displayData.forEach((uni, index) => {
        const card = document.createElement('div');
        card.className = 'card';
        // card.style.cursor = 'pointer'; // Removed to allow interaction with checkbox

        // Image logic
        const imageHtml = uni.image ? `<div class="card-image" style="background-image: url('${uni.image}')"></div>` : `<div class="card-image placeholder"></div>`;

        // Check if selected for compare
        const isChecked = compareList.includes(uni.name) ? 'checked' : '';
        const isFav = favorites.includes(uni.name) ? 'active' : '';

        card.innerHTML = `
            ${imageHtml}
            
            <div class="card-actions-top">
                <div class="compare-checkbox-container" title="Compare">
                    <input type="checkbox" class="compare-checkbox" data-name="${uni.name}" ${isChecked}>
                </div>
                <button class="favorite-btn ${isFav}" data-name="${uni.name}" title="Add to Favorites">
                    ❤️
                </button>
            </div>

            <div class="rank-badge">#${uni.rank}</div>
            
            <div class="card-header">
                <div class="card-location">
                    <span>${uni.country}</span> • <span>${uni.city}</span> • <span>📏 ${uni.distance_tul} km</span>
                </div>
                
                <div class="weather-widget" title="Average June Temperature">
                    ☀️ ${uni.weather_june}°C
                </div>

                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 5px;">
                    <div class="grant-badge" title="Monthly Erasmus+ Grant">
                        💶 €${uni.grant} / month
                    </div>
                     <div class="grant-badge" style="background: rgba(108, 92, 231, 0.15); color: #a29bfe; border-color: rgba(108, 92, 231, 0.3);" title="Global University Ranking (Approx)">
                        🌐 Global Rank: ${uni.global_rank}
                    </div>
                </div>
                <!-- Z-index fix: ensure link is above other elements -->
                <h2>${uni.name}</h2>
                <style>
                    /* .card h2 a:hover { border-color: var(--gold); } */
                </style>
                <div class="fields-list">
                    ${uni.fields.map(f => `
                        <div class="field-item">
                            <div style="display:flex; flex-direction:column;">
                                <span class="field-name">${f.name}</span>
                                <span class="field-lang" style="font-size: 0.75em; color: #a29bfe; margin-top: 2px;">🗣️ ${f.language || 'Unknown'}</span>
                            </div>
                            <span class="field-places">${f.places} places</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="tags">
                ${uni.tags.map(tag => `<span class="tag highlight">${tag}</span>`).join('')}
                <span class="tag">Erasmus+</span>
            </div>
            
            <div class="stats-grid">
                <div class="stat">
                    <span class="stat-label">Vibe</span>
                    <span class="stat-value ${getColorClass(uni.scores.vibe)}">${uni.scores.vibe}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Academic</span>
                    <span class="stat-value ${getColorClass(uni.scores.academic)}">${uni.scores.academic}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Cost</span>
                    <span class="stat-value ${getColorClass(uni.scores.cost)}">${uni.scores.cost}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Location</span>
                    <span class="stat-value ${getColorClass(uni.scores.location)}">${uni.scores.location}</span>
                </div>
                <div class="stat total-score">
                    <span class="stat-label">Total Score</span>
                    <span class="stat-value">${uni.scores.total}</span>
                </div>
            </div>
`;

        // Stagger animation
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        container.appendChild(card);

        // Event for checkbox
        const checkbox = card.querySelector('.compare-checkbox');
        checkbox.addEventListener('change', (e) => {
            e.stopPropagation(); // Prevent card click
            toggleCompare(uni.name, e.target.checked);
        });

        // Event for favorite
        const favBtn = card.querySelector('.favorite-btn');
        favBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFavorite(uni.name);
        });

        // Event for card click (optional details view? for now just log)
        /* card.addEventListener('click', () => {
             console.log("Clicked card:", uni.name);
        }); */

        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50); // Stagger by 50ms
    });
}

function getColorClass(score) {
    if (score >= 8.0) return 'high';
    if (score >= 6.0) return 'med';
    return '';
}

favoritesBtn.addEventListener('click', () => {
    showFavoritesOnly = !showFavoritesOnly;
    favoritesBtn.classList.toggle('active');

    // Switch to list view if in map view
    if (mapViewBtn.classList.contains('active')) {
        listViewBtn.click();
    }

    renderCards(currentData);
});

// --- Comparator Logic ---

function toggleCompare(uniName, isChecked) {
    if (isChecked) {
        if (compareList.length >= 2) {
            alert("You can compare max 2 universities!");
            renderCards(currentData); // specific re-render to uncheck? cleaner to just prevent
            return;
        }
        compareList.push(uniName);
    } else {
        compareList = compareList.filter(n => n !== uniName);
    }
    updateCompareUI();
}

function updateCompareUI() {
    compareCount.textContent = compareList.length;
    if (compareList.length > 0) {
        compareFab.style.display = 'flex';
    } else {
        compareFab.style.display = 'none';
    }
}

compareFab.addEventListener('click', () => {
    if (compareList.length < 2) {
        alert("Select 2 universities to compare!");
        return;
    }
    openComparisonModal();
});

function openComparisonModal() {
    const uni1 = universities.find(u => u.name === compareList[0]);
    const uni2 = universities.find(u => u.name === compareList[1]);

    if (!uni1 || !uni2) return;

    compareGrid.innerHTML = `
        ${renderCompareCard(uni1, uni2)}
        ${renderCompareCard(uni2, uni1)}
`;

    compareModal.style.display = 'block';
}

function renderCompareCard(uni, opponent) {
    const winClass = (score, oppScore) => (score > oppScore ? 'winner' : (score < oppScore ? 'loser' : ''));

    // Calculate total places
    const totalPlaces = uni.fields.reduce((acc, f) => acc + parseInt(f.places), 0);
    const oppTotalPlaces = opponent.fields.reduce((acc, f) => acc + parseInt(f.places), 0);

    return `
    < div class="compare-card" >
            <h3>${uni.name}</h3>
            <p style="color: #bbb; margin-bottom: 1rem;">${uni.city}, ${uni.country}</p>
            
            <div class="compare-row">
                <span class="compare-label">Total Score</span>
                <span class="compare-value ${winClass(uni.scores.total, opponent.scores.total)}">${uni.scores.total}</span>
            </div>
            <div class="compare-row">
                <span class="compare-label">Global Rank 🌐</span>
                <span class="compare-value ${winClass(opponent.global_rank, uni.global_rank)}">#${uni.global_rank}</span>
            </div>
            <div class="compare-row">
                <span class="compare-label">Monthly Grant</span>
                <span class="compare-value ${winClass(uni.grant, opponent.grant)}">€${uni.grant}</span>
            </div>
             <div class="compare-row">
                <span class="compare-label">Total Places</span>
                <span class="compare-value ${winClass(totalPlaces, oppTotalPlaces)}">${totalPlaces}</span>
            </div>
            <div class="compare-row">
                <span class="compare-label">Vibe</span>
                <span class="compare-value ${winClass(uni.scores.vibe, opponent.scores.vibe)}">${uni.scores.vibe}</span>
            </div>
            <div class="compare-row">
                <span class="compare-label">Academic</span>
                <span class="compare-value ${winClass(uni.scores.academic, opponent.scores.academic)}">${uni.scores.academic}</span>
            </div>
            <div class="compare-row">
                <span class="compare-label">Cost</span>
                <span class="compare-value ${winClass(uni.scores.cost, opponent.scores.cost)}">${uni.scores.cost}</span>
            </div>
        </div >
    `;
}

// Modal Close
closeModal.addEventListener('click', () => {
    compareModal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target == compareModal) {
        compareModal.style.display = 'none';
    }
});


// --- Filtering & View Toggles ---

// Search Functionality
searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = universities.filter(uni =>
        uni.name.toLowerCase().includes(term) ||
        uni.city.toLowerCase().includes(term) ||
        uni.country.toLowerCase().includes(term)
    );
    currentData = filtered; // Update current dataset state
    renderCards(filtered);
    updateMapMarkers(filtered);
});

// Sorting Functionality
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const sortKey = btn.dataset.sort;
        let sorted = [...currentData]; // Sort current subset

        if (sortKey === 'total') {
            sorted.sort((a, b) => b.scores.total - a.scores.total);
        } else {
            sorted.sort((a, b) => b.scores[sortKey] - a.scores[sortKey]);
        }

        // Update currentData order? Or just render?
        // Better to just render.
        renderCards(sorted);
    });
});

// View Toggle
listViewBtn.addEventListener('click', () => {
    listViewBtn.classList.add('active');
    mapViewBtn.classList.remove('active');

    container.style.display = 'grid'; // Grid is for list/cards
    mapContainer.style.display = 'none';
});

mapViewBtn.addEventListener('click', () => {
    mapViewBtn.classList.add('active');
    listViewBtn.classList.remove('active');

    container.style.display = 'none';
    mapContainer.style.display = 'block';

    initMap();
    updateMapMarkers(currentData);
    map.invalidateSize(); // Fix leafleft rendering issue on show
});


// Initial Render
renderCards(currentData);
