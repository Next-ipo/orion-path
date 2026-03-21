// Ippo Experience Hub - Main Logic

document.addEventListener('DOMContentLoaded', () => {
    renderNoteCards();
});

/**
 * Note記事の動的表示（設計図に基づいた主要記事）
 */
function renderNoteCards() {
    const noteList = document.getElementById('note-list');
    const articles = [
        { date: "2026.03.08", title: "ロケット見学と至高 of 体験投資", tag: "Magazine", url: "https://note.com/next_ipo" },
        { date: "2026.02.26", title: "カイロスロケット。和歌山奇跡のリトリート", tag: "Travel", url: "https://note.com/next_ipo/n/n5d46266b86ef" },
        { date: "2026.02.14", title: "電脳の海へ。ARグラス越しに見た未来", tag: "Tech", url: "https://note.com/next_ipo/n/nbe17f9a012ce" },
        { date: "2026.02.08", title: "ゴジラホテル。巨大な熱量に触れる夜", tag: "Experience", url: "https://note.com/next_ipo/n/n203c41d6e20d" }
    ];

    noteList.innerHTML = articles.map(art => `
        <a href="${art.url}" target="_blank" class="note-item" style="display: block; text-decoration: none; color: inherit; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease;">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.25rem;">
                <span style="font-size: 0.75rem; color: var(--accent-blue); opacity: 0.8; font-family: var(--font-main);">${art.date}</span>
                <span style="font-size: 0.65rem; padding: 0.1rem 0.4rem; border: 1px solid var(--accent-blue); color: var(--accent-blue); border-radius: 2px;">${art.tag}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.95rem; font-weight: 500;">${art.title}</span>
            </div>
        </a>
    `).join('');
}

// Scroll Reveal Simple implementation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.card').forEach(card => observer.observe(card));
