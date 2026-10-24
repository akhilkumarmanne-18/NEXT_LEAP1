/**
 * NEXT LEAP 2.0 - Learning Roadmap JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    setupTaskToggles();
    setupAddCustomTaskModal();
    setupRegenerateRoadmap();
});

function setupTaskToggles() {
    const checkboxes = document.querySelectorAll('.roadmap-task-checkbox');
    checkboxes.forEach(cb => {
        cb.addEventListener('change', async (e) => {
            const taskId = cb.dataset.taskId;
            try {
                const res = await fetch(`/api/roadmap/task/toggle/${taskId}`, { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    const taskItem = document.getElementById(`task-item-${taskId}`);
                    const taskTitle = document.getElementById(`task-title-${taskId}`);
                    
                    if (data.new_status === 'Completed') {
                        taskTitle.classList.add('completed');
                        if (taskItem) taskItem.classList.add('task-completed');
                    } else {
                        taskTitle.classList.remove('completed');
                        if (taskItem) taskItem.classList.remove('task-completed');
                    }

                    // Update Phase Progress Bar
                    const phaseBar = document.getElementById(`phase-progress-${cb.dataset.phaseId}`);
                    const phaseText = document.getElementById(`phase-text-${cb.dataset.phaseId}`);
                    if (phaseBar) phaseBar.style.width = `${data.phase_progress}%`;
                    if (phaseText) phaseText.innerText = `${data.phase_progress}%`;

                    // Update Overall Roadmap Progress
                    const overallBar = document.getElementById('overallRoadmapBar');
                    const overallText = document.getElementById('overallRoadmapText');
                    if (overallBar) overallBar.style.width = `${data.roadmap_progress}%`;
                    if (overallText) overallText.innerText = `${data.roadmap_progress}%`;

                    showToast(`Milestone marked as ${data.new_status}`, 'success');
                }
            } catch (err) {
                showToast('Failed to update milestone status', 'error');
            }
        });
    });
}

function setupAddCustomTaskModal() {
    const modal = document.getElementById('customTaskModal');
    const openBtns = document.querySelectorAll('.open-add-task-btn');
    const closeBtn = document.getElementById('closeCustomTaskModal');
    const submitBtn = document.getElementById('submitCustomTaskBtn');

    openBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const phaseId = btn.dataset.phaseId;
            document.getElementById('taskPhaseId').value = phaseId;
            modal.classList.add('active');
        });
    });

    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', async () => {
            const phaseId = document.getElementById('taskPhaseId').value;
            const title = document.getElementById('taskTitleInput').value.trim();
            const description = document.getElementById('taskDescInput').value.trim();
            const skills = document.getElementById('taskSkillsInput').value.trim();
            const hours = document.getElementById('taskHoursInput').value;
            const targetDate = document.getElementById('taskDateInput').value;

            if (!title) {
                showToast('Task title is required', 'warning');
                return;
            }

            submitBtn.disabled = true;
            submitBtn.innerText = 'Adding...';

            try {
                const res = await fetch('/api/roadmap/task/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        phase_id: phaseId,
                        title,
                        description,
                        skills_involved: skills,
                        estimated_hours: hours,
                        target_date: targetDate
                    })
                });
                const data = await res.json();
                if (data.success) {
                    showToast('Custom learning task added!', 'success');
                    modal.classList.remove('active');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(data.message || 'Error adding task', 'error');
                }
            } catch (err) {
                showToast('Network error adding task', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = 'Save Task';
            }
        });
    }
}

function setupRegenerateRoadmap() {
    const regenBtn = document.getElementById('regenerateRoadmapBtn');
    if (!regenBtn) return;

    regenBtn.addEventListener('click', async () => {
        if (!confirm('Regenerating will recalculate your milestones based on your target career. Proceed?')) return;

        regenBtn.disabled = true;
        regenBtn.innerText = 'Calibrating...';

        try {
            const res = await fetch('/api/roadmap/regenerate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                setTimeout(() => window.location.reload(), 1000);
            }
        } catch (err) {
            showToast('Failed to regenerate roadmap', 'error');
        } finally {
            regenBtn.disabled = false;
            regenBtn.innerText = 'Recalibrate Roadmap';
        }
    });
}
