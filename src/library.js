// Celestial Library Logic

document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('src/celestial_data.json');
    const data = await response.json();

    renderGallery(data['宇宙美術館']);
    renderTimeline(data['2026年おススメ天体現象']);
    renderApps(data['おススメアプリ']);
    initSeasonalTabs(data['季節の星座・天体データベース']);
    initFilters(data['宇宙美術館']);
});

function renderGallery(items, filter = 'all') {
    const gallery = document.getElementById('messier-gallery');
    const filteredItems = filter === 'all' 
        ? items 
        : items.filter(item => item.Type.includes(filter));

    gallery.innerHTML = filteredItems.map(item => `
        <div class="celestial-card glass fade-in">
            ${item.Image ? 
                `<img src="${item.Image}" alt="${item.Name}" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.8;">` :
                `<div style="background: rgba(0,0,0,0.5); width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: rgba(255,255,255,0.1); font-weight: 800;">
                    ${item.Name}
                </div>`
            }
            <div class="celestial-info">
                <div style="font-weight: 800; color: var(--accent-blue);">${item.Name}</div>
                <div style="font-size: 0.8rem; color: #fff;">${item.Constellation}</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">${item.Type}</div>
            </div>
        </div>
    `).join('');
}

function renderTimeline(events) {
    const timeline = document.getElementById('event-timeline');
    timeline.innerHTML = events.map(event => `
        <div class="timeline-item">
            <div style="font-family: var(--font-main); color: var(--accent-blue); font-size: 0.8rem;">${event['Date/Period']}</div>
            <div style="font-weight: 500; font-size: 1.1rem; margin-top: 0.2rem;">${event.Event}</div>
        </div>
    `).join('');
}

function renderApps(apps) {
    const grid = document.getElementById('app-grid');
    grid.innerHTML = apps.map(app => `
        <div class="card glass app-card">
            <h3 style="color: var(--accent-green); margin-bottom: 0.5rem; font-size: 1.1rem;">${app.Name}</h3>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">${app.Description}</p>
            ${app.Link ? `<a href="${app.Link}" target="_blank" class="filter-btn" style="display: block; width: 100%;">Visit Tool</a>` : ''}
        </div>
    `).join('');
}

function initSeasonalTabs(db) {
    const buttons = document.querySelectorAll('.tab-btn');
    const tbody = document.getElementById('seasonal-tbody');

    const renderSeason = (season) => {
        const filtered = db.filter(item => item.Season === season);
        tbody.innerHTML = filtered.map(item => `
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 1rem; font-weight: 500;">${item.Name}</td>
                <td style="padding: 1rem;">${item.Constellation}</td>
                <td style="padding: 1rem; color: var(--text-secondary);">${item.Type}</td>
                <td style="padding: 1rem; font-style: italic; color: var(--accent-green); font-size: 0.8rem;">${item.Alias || '-'}</td>
            </tr>
        `).join('');
    };

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderSeason(btn.dataset.season);
        });
    });

    renderSeason('春');
}

function initFilters(items) {
    const buttons = document.querySelectorAll('.filter-btn[data-filter]');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderGallery(items, btn.dataset.filter);
        });
    });
}
