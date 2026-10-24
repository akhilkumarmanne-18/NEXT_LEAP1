/**
 * NEXT LEAP 2.0 - Core Application JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // 2. Initialize Theme
    initTheme();

    // 3. Mobile Sidebar Toggle
    const mobileToggle = document.getElementById('mobileSidebarToggle');
    const sidebar = document.querySelector('.app-sidebar');
    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // 4. Notifications Dropdown Toggle
    const notifBtn = document.getElementById('notifDropdownBtn');
    const notifMenu = document.getElementById('notifDropdownMenu');
    if (notifBtn && notifMenu) {
        notifBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notifMenu.classList.toggle('show');
        });
        document.addEventListener('click', () => {
            notifMenu.classList.remove('show');
        });
    }

    // 5. Global Search in Topbar
    const searchInput = document.getElementById('globalSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (!query) return;
            // Quick match navigation shortcuts
            if (query === 'careers' || query === 'jobs') window.location.href = '/careers';
            if (query === 'skills' || query === 'gap') window.location.href = '/skill-gap';
            if (query === 'roadmap' || query === 'learning') window.location.href = '/roadmap';
            if (query === 'projects' || query === 'studio') window.location.href = '/projects';
            if (query === 'interview' || query === 'prep') window.location.href = '/interviews';
            if (query === 'coach' || query === 'ai') window.location.href = '/coach';
        });
    }

    // 6. FAQ Accordion for Landing Page
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                faqItems.forEach(i => i.classList.remove('active'));
                if (!isActive) item.classList.add('active');
            });
        }
    });
});

/**
 * Theme Management (Dark / Light)
 */
function initTheme() {
    const savedTheme = localStorage.getItem('nextleap_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    const themeToggleBtn = document.getElementById('themeToggleBtn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', nextTheme);
            localStorage.setItem('nextleap_theme', nextTheme);
            updateThemeIcon(nextTheme);

            // Sync with backend if user is logged in
            fetch('/api/settings/theme', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ theme: nextTheme })
            }).catch(() => {});
        });
    }
}

function updateThemeIcon(theme) {
    const iconSpan = document.getElementById('themeIcon');
    if (!iconSpan) return;
    if (theme === 'light') {
        iconSpan.innerHTML = '<i data-lucide="sun"></i>';
    } else {
        iconSpan.innerHTML = '<i data-lucide="moon"></i>';
    }
    if (window.lucide) lucide.createIcons();
}

/**
 * Global Toast Alert
 */
function showToast(message, type = 'info') {
    let container = document.querySelector('.alert-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'alert-container';
        document.body.appendChild(container);
    }

    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'error' ? 'danger' : type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button style="background:none;border:none;color:inherit;cursor:pointer;font-size:1.1rem;margin-left:12px;" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(alert);
    setTimeout(() => {
        if (alert.parentElement) alert.remove();
    }, 4500);
}
