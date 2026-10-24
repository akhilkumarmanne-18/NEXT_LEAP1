/**
 * NEXT LEAP 2.0 - Project Studio & Portfolio JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    setupStartProjectButtons();
    setupProjectSliders();
    setupPortfolioToggles();
});

function setupStartProjectButtons() {
    const startBtns = document.querySelectorAll('.btn-start-project');
    startBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const projectId = btn.dataset.projectId;
            btn.disabled = true;
            btn.innerText = 'Starting...';

            try {
                const res = await fetch(`/api/projects/start/${projectId}`, { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    showToast(data.message, 'success');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast(data.message || 'Error starting project', 'error');
                    btn.disabled = false;
                    btn.innerText = 'Start Project';
                }
            } catch (err) {
                showToast('Failed to start project', 'error');
                btn.disabled = false;
                btn.innerText = 'Start Project';
            }
        });
    });
}

function setupProjectSliders() {
    const saveBtns = document.querySelectorAll('.btn-save-project-progress');
    saveBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const upId = btn.dataset.upId;
            const slider = document.getElementById(`progress-slider-${upId}`);
            const notesInput = document.getElementById(`notes-input-${upId}`);
            const repoInput = document.getElementById(`repo-input-${upId}`);
            const liveInput = document.getElementById(`live-input-${upId}`);

            const progress = slider ? slider.value : 0;
            const notes = notesInput ? notesInput.value : '';
            const repo_url = repoInput ? repoInput.value : '';
            const live_url = liveInput ? liveInput.value : '';

            btn.disabled = true;
            btn.innerText = 'Saving...';

            try {
                const res = await fetch(`/api/projects/update/${upId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        progress_percent: progress,
                        notes,
                        repo_url,
                        live_url,
                        status: parseInt(progress) === 100 ? 'Completed' : 'In Progress'
                    })
                });
                const data = await res.json();
                if (data.success) {
                    showToast('Project progress saved successfully!', 'success');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(data.message || 'Error updating project', 'error');
                }
            } catch (err) {
                showToast('Failed to save progress', 'error');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Save Progress';
            }
        });
    });
}

function setupPortfolioToggles() {
    const portfolioBtns = document.querySelectorAll('.btn-toggle-portfolio');
    portfolioBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const upId = btn.dataset.upId;
            try {
                const res = await fetch(`/api/projects/toggle-portfolio/${upId}`, { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    showToast(data.message, 'success');
                    if (data.in_portfolio) {
                        btn.classList.remove('btn-secondary');
                        btn.classList.add('btn-primary');
                        btn.innerText = 'In Portfolio';
                    } else {
                        btn.classList.remove('btn-primary');
                        btn.classList.add('btn-secondary');
                        btn.innerText = 'Add to Portfolio';
                    }
                }
            } catch (err) {
                showToast('Error updating portfolio status', 'error');
            }
        });
    });
}
