/**
 * NEXT LEAP 2.0 - Dashboard Interactive Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    setupNextAction();
    setupDashboardTaskCheckboxes();
});

function initCharts() {
    // 1. Weekly Learning Activity Chart
    const weeklyCanvas = document.getElementById('weeklyActivityChart');
    if (weeklyCanvas && window.Chart) {
        const ctx = weeklyCanvas.getContext('2d');
        const days = JSON.parse(weeklyCanvas.dataset.days || '["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]');
        const actualHours = JSON.parse(weeklyCanvas.dataset.actual || '[1.5, 2.0, 1.0, 2.5, 3.0, 2.0, 1.5]');
        const targetHours = JSON.parse(weeklyCanvas.dataset.target || '[1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7]');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: days,
                datasets: [
                    {
                        label: 'Study Hours',
                        data: actualHours,
                        backgroundColor: 'rgba(79, 124, 255, 0.85)',
                        borderColor: '#4F7CFF',
                        borderWidth: 1,
                        borderRadius: 6
                    },
                    {
                        type: 'line',
                        label: 'Target Pace',
                        data: targetHours,
                        borderColor: '#8B5CF6',
                        borderWidth: 2,
                        borderDash: [4, 4],
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#94A3B8', font: { family: 'Inter' } }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94A3B8', font: { family: 'Inter' } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94A3B8', font: { family: 'Inter' } }
                    }
                }
            }
        });
    }

    // 2. Career Readiness Radar / Bar Chart
    const readinessCanvas = document.getElementById('readinessRadarChart');
    if (readinessCanvas && window.Chart) {
        const ctx = readinessCanvas.getContext('2d');
        const labels = JSON.parse(readinessCanvas.dataset.labels || '["Python","SQL","Statistics","Machine Learning","Visualization"]');
        const userData = JSON.parse(readinessCanvas.dataset.user || '[2, 0, 1, 0, 1]');
        const targetData = JSON.parse(readinessCanvas.dataset.target || '[2, 2, 2, 2, 1]');

        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Your Current Level',
                        data: userData,
                        backgroundColor: 'rgba(79, 124, 255, 0.25)',
                        borderColor: '#4F7CFF',
                        pointBackgroundColor: '#4F7CFF',
                        borderWidth: 2
                    },
                    {
                        label: 'Target Requirement',
                        data: targetData,
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderColor: 'rgba(139, 92, 246, 0.7)',
                        borderDash: [3, 3],
                        pointBackgroundColor: '#8B5CF6',
                        borderWidth: 1.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#94A3B8', font: { family: 'Inter' } }
                    }
                },
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
                        grid: { color: 'rgba(255, 255, 255, 0.08)' },
                        pointLabels: { color: '#94A3B8', font: { family: 'Inter', size: 11 } },
                        ticks: { display: false, min: 0, max: 3, stepSize: 1 }
                    }
                }
            }
        });
    }
}

function setupNextAction() {
    const completeBtn = document.getElementById('btnCompleteNextAction');
    if (!completeBtn) return;

    completeBtn.addEventListener('click', async () => {
        const actionId = completeBtn.dataset.actionId;
        if (!actionId) return;

        completeBtn.disabled = true;
        completeBtn.innerText = 'Updating...';

        try {
            const res = await fetch('/api/next-action/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action_id: actionId })
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                // Dynamically update the Next LEAP Card content without page refresh
                const cardTitle = document.getElementById('nextActionTitle');
                const cardReason = document.getElementById('nextActionReason');
                const cardEffort = document.getElementById('nextActionEffort');
                const cardPriority = document.getElementById('nextActionPriority');
                const cardCta = document.getElementById('nextActionCta');

                if (data.next_action) {
                    if (cardTitle) cardTitle.innerText = data.next_action.title;
                    if (cardReason) cardReason.innerText = data.next_action.reason;
                    if (cardEffort) cardEffort.innerText = data.next_action.estimated_effort;
                    if (cardPriority) cardPriority.innerText = data.next_action.priority;
                    if (cardCta) {
                        cardCta.href = data.next_action.cta_url;
                        cardCta.innerText = data.next_action.cta_label;
                    }
                    completeBtn.dataset.actionId = data.next_action.id;
                    completeBtn.innerText = 'Mark Done & Next';
                    completeBtn.disabled = false;
                } else {
                    completeBtn.innerText = 'All Caught Up!';
                }
            } else {
                showToast(data.message || 'Error completing action', 'error');
                completeBtn.disabled = false;
                completeBtn.innerText = 'Mark Done & Next';
            }
        } catch (err) {
            showToast('Network error while completing action', 'error');
            completeBtn.disabled = false;
            completeBtn.innerText = 'Mark Done & Next';
        }
    });
}

function setupDashboardTaskCheckboxes() {
    const checkboxes = document.querySelectorAll('.dashboard-task-checkbox');
    checkboxes.forEach(cb => {
        cb.addEventListener('change', async (e) => {
            const taskId = cb.dataset.taskId;
            try {
                const res = await fetch(`/api/roadmap/task/toggle/${taskId}`, { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    const titleSpan = document.getElementById(`dash-task-title-${taskId}`);
                    if (titleSpan) {
                        if (data.new_status === 'Completed') {
                            titleSpan.classList.add('completed');
                        } else {
                            titleSpan.classList.remove('completed');
                        }
                    }
                    showToast(`Task status updated to ${data.new_status}`, 'success');
                }
            } catch (err) {
                showToast('Failed to update task', 'error');
            }
        });
    });
}
