/**
 * NEXT LEAP 2.0 - Career Discovery & Comparison JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    setupCareerFilters();
    setupTargetCareerButtons();
    setupComparisonModal();
    setupDiscoveryQuizModal();
});

function setupCareerFilters() {
    const filterBtns = document.querySelectorAll('.category-filter-btn');
    const careerCards = document.querySelectorAll('.career-match-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('btn-primary'));
            filterBtns.forEach(b => b.classList.add('btn-secondary'));
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-primary');

            const cat = btn.dataset.category;
            careerCards.forEach(card => {
                if (cat === 'All' || card.dataset.category === cat) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

function setupTargetCareerButtons() {
    const setTargetBtns = document.querySelectorAll('.btn-set-target');
    setTargetBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const careerId = btn.dataset.careerId;
            btn.disabled = true;
            btn.innerText = 'Setting...';

            try {
                const res = await fetch(`/api/careers/set-target/${careerId}`, { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    showToast(data.message, 'success');
                    // Reload to update roadmap & dashboard active state
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast(data.message || 'Error setting target career', 'error');
                    btn.disabled = false;
                    btn.innerText = 'Set as Target';
                }
            } catch (err) {
                showToast('Network error setting target career', 'error');
                btn.disabled = false;
                btn.innerText = 'Set as Target';
            }
        });
    });
}

function setupComparisonModal() {
    const compareBtn = document.getElementById('openCompareBtn');
    const modal = document.getElementById('compareModal');
    const closeBtn = document.getElementById('closeCompareModal');
    const executeBtn = document.getElementById('executeCompareBtn');

    if (compareBtn && modal) {
        compareBtn.addEventListener('click', () => modal.classList.add('active'));
    }
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }

    if (executeBtn) {
        executeBtn.addEventListener('click', async () => {
            const c1 = document.getElementById('compareSelect1').value;
            const c2 = document.getElementById('compareSelect2').value;

            if (c1 === c2) {
                showToast('Please select two different careers to compare', 'warning');
                return;
            }

            executeBtn.disabled = true;
            executeBtn.innerText = 'Comparing...';

            try {
                const res = await fetch(`/api/careers/compare?c1=${c1}&c2=${c2}`);
                const data = await res.json();
                if (data.success) {
                    renderComparisonResults(data.data);
                } else {
                    showToast(data.message, 'error');
                }
            } catch (err) {
                showToast('Failed to compare careers', 'error');
            } finally {
                executeBtn.disabled = false;
                executeBtn.innerText = 'Compare';
            }
        });
    }
}

function renderComparisonResults(data) {
    const resultsContainer = document.getElementById('comparisonResults');
    if (!resultsContainer) return;

    const c1 = data.career_1;
    const c2 = data.career_2;

    resultsContainer.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px;">
            <div class="card" style="border-top:4px solid var(--accent-primary);">
                <h4>${c1.career.title}</h4>
                <div class="badge badge-primary" style="margin:8px 0;">Readiness: ${c1.readiness}%</div>
                <p style="font-size:0.875rem;color:var(--text-secondary);margin:8px 0;"><strong>Salary:</strong> ${c1.career.salary_range}</p>
                <p style="font-size:0.875rem;color:var(--text-secondary);margin:8px 0;"><strong>Outlook:</strong> ${c1.career.market_outlook}</p>
                <h5 style="margin-top:14px;font-size:0.9rem;">Skills Matched:</h5>
                <p style="font-size:0.85rem;color:var(--success);">${c1.matched_skills.join(', ') || 'None'}</p>
                <h5 style="margin-top:10px;font-size:0.9rem;">Missing Skills:</h5>
                <p style="font-size:0.85rem;color:var(--danger);">${c1.missing_skills.join(', ') || 'None'}</p>
            </div>

            <div class="card" style="border-top:4px solid var(--accent-secondary);">
                <h4>${c2.career.title}</h4>
                <div class="badge badge-violet" style="margin:8px 0;">Readiness: ${c2.readiness}%</div>
                <p style="font-size:0.875rem;color:var(--text-secondary);margin:8px 0;"><strong>Salary:</strong> ${c2.career.salary_range}</p>
                <p style="font-size:0.875rem;color:var(--text-secondary);margin:8px 0;"><strong>Outlook:</strong> ${c2.career.market_outlook}</p>
                <h5 style="margin-top:14px;font-size:0.9rem;">Skills Matched:</h5>
                <p style="font-size:0.85rem;color:var(--success);">${c2.matched_skills.join(', ') || 'None'}</p>
                <h5 style="margin-top:10px;font-size:0.9rem;">Missing Skills:</h5>
                <p style="font-size:0.85rem;color:var(--danger);">${c2.missing_skills.join(', ') || 'None'}</p>
            </div>
        </div>
    `;
}

function setupDiscoveryQuizModal() {
    const quizBtn = document.getElementById('openQuizBtn');
    const modal = document.getElementById('quizModal');
    const closeBtn = document.getElementById('closeQuizModal');
    const submitBtn = document.getElementById('submitQuizBtn');

    if (quizBtn && modal) {
        quizBtn.addEventListener('click', () => modal.classList.add('active'));
    }
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', async () => {
            const interests = document.getElementById('quizInterests').value;
            const course = document.getElementById('quizCourse').value;
            const learningStyle = document.getElementById('quizLearningStyle').value;
            const skillsStr = document.getElementById('quizSkills').value;
            const skills = skillsStr.split(',').map(s => s.trim()).filter(Boolean);

            submitBtn.disabled = true;
            submitBtn.innerText = 'Calculating Fit...';

            try {
                const res = await fetch('/api/careers/discovery-quiz', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        interests,
                        course,
                        learning_style: learningStyle,
                        skills
                    })
                });
                const data = await res.json();
                if (data.success && data.matches) {
                    showToast('Career matches calculated based on your responses!', 'success');
                    modal.classList.remove('active');
                    // Re-render matches on page
                    renderQuizMatches(data.matches);
                }
            } catch (err) {
                showToast('Failed to run discovery quiz', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = 'Calculate Recommendations';
            }
        });
    }
}

function renderQuizMatches(matches) {
    const list = document.getElementById('careerMatchesList');
    if (!list) return;

    list.innerHTML = matches.map(m => `
        <div class="card career-match-card" data-category="${m.career.category}" style="margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                <div>
                    <span class="badge badge-primary">${m.career.category}</span>
                    <h3 style="margin-top:6px;">${m.career.title}</h3>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.6rem;font-weight:800;color:var(--accent-primary);">${m.match_score}%</div>
                    <span class="badge ${m.match_score >= 75 ? 'badge-success' : 'badge-warning'}">${m.recommendation_tag}</span>
                </div>
            </div>
            <p style="color:var(--text-secondary);font-size:0.925rem;margin-bottom:16px;">${m.career.description}</p>
            <div style="display:flex;gap:12px;align-items:center;">
                <a href="/careers/${m.career.slug}" class="btn btn-secondary btn-sm">Explore Details</a>
                <button class="btn btn-primary btn-sm btn-set-target" data-career-id="${m.career.id}">Set as Target Career</button>
            </div>
        </div>
    `).join('');
    setupTargetCareerButtons();
}
