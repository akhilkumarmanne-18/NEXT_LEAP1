/**
 * NEXT LEAP 2.0 - Interview Preparation JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    setupQuizOptions();
    setupMockInterviewSubmission();
});

function setupQuizOptions() {
    const quizOptions = document.querySelectorAll('.quiz-option-btn');
    quizOptions.forEach(opt => {
        opt.addEventListener('click', async () => {
            const questionId = opt.dataset.questionId;
            const selectedText = opt.innerText.trim();
            const parentCard = opt.closest('.quiz-card');

            // Disable siblings
            parentCard.querySelectorAll('.quiz-option-btn').forEach(b => b.disabled = true);

            try {
                const res = await fetch('/api/interviews/check-quiz', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question_id: questionId,
                        selected_option: selectedText
                    })
                });
                const data = await res.json();
                const feedbackDiv = parentCard.querySelector('.quiz-feedback');

                if (data.is_correct) {
                    opt.style.background = 'var(--success-bg)';
                    opt.style.borderColor = 'var(--success)';
                    opt.style.color = 'var(--success)';
                    feedbackDiv.innerHTML = `
                        <div class="badge badge-success" style="margin-bottom:8px;">Correct Answer!</div>
                        <p style="font-size:0.875rem;color:var(--text-secondary);">${data.explanation || ''}</p>
                    `;
                } else {
                    opt.style.background = 'var(--danger-bg)';
                    opt.style.borderColor = 'var(--danger)';
                    opt.style.color = 'var(--danger)';
                    feedbackDiv.innerHTML = `
                        <div class="badge badge-danger" style="margin-bottom:8px;">Incorrect</div>
                        <p style="font-size:0.875rem;color:var(--text-secondary);"><strong>Correct answer:</strong> ${data.correct_answer}. ${data.explanation || ''}</p>
                    `;
                }
                feedbackDiv.style.display = 'block';
            } catch (err) {
                showToast('Failed to verify answer', 'error');
            }
        });
    });
}

function setupMockInterviewSubmission() {
    const submitBtns = document.querySelectorAll('.btn-submit-mock-answer');
    submitBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const questionId = btn.dataset.questionId;
            const textarea = document.getElementById(`answer-text-${questionId}`);
            const resultContainer = document.getElementById(`eval-result-${questionId}`);

            const answer = textarea ? textarea.value.trim() : '';
            if (!answer) {
                showToast('Please type your response before submitting.', 'warning');
                return;
            }

            btn.disabled = true;
            btn.innerText = 'Evaluating with Rubric...';

            try {
                const res = await fetch('/api/interviews/submit-answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question_id: questionId,
                        answer: answer
                    })
                });
                const data = await res.json();
                if (data.success) {
                    showToast('Response evaluated and rubric generated!', 'success');
                    resultContainer.style.display = 'block';
                    resultContainer.innerHTML = `
                        <div style="background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:var(--radius-sm);padding:20px;margin-top:16px;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                                <h4 style="font-size:1.1rem;">Mock Evaluation Result</h4>
                                <div style="font-size:1.6rem;font-weight:800;color:${data.score >= 75 ? 'var(--success)' : 'var(--warning)'};">${data.score}%</div>
                            </div>
                            <p style="font-size:0.925rem;color:var(--text-primary);margin-bottom:16px;line-height:1.6;">${data.feedback}</p>

                            <!-- Criteria Breakdown -->
                            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px;">
                                <div style="background:var(--bg-card);padding:10px;border-radius:6px;text-align:center;">
                                    <span style="font-size:0.75rem;color:var(--text-muted);display:block;">Relevance</span>
                                    <strong style="color:var(--accent-primary);">${data.criteria.relevance}/25</strong>
                                </div>
                                <div style="background:var(--bg-card);padding:10px;border-radius:6px;text-align:center;">
                                    <span style="font-size:0.75rem;color:var(--text-muted);display:block;">Clarity</span>
                                    <strong style="color:var(--accent-primary);">${data.criteria.clarity}/25</strong>
                                </div>
                                <div style="background:var(--bg-card);padding:10px;border-radius:6px;text-align:center;">
                                    <span style="font-size:0.75rem;color:var(--text-muted);display:block;">Completeness</span>
                                    <strong style="color:var(--accent-primary);">${data.criteria.completeness}/25</strong>
                                </div>
                                <div style="background:var(--bg-card);padding:10px;border-radius:6px;text-align:center;">
                                    <span style="font-size:0.75rem;color:var(--text-muted);display:block;">Technical Rigor</span>
                                    <strong style="color:var(--accent-primary);">${data.criteria.technical_correctness}/25</strong>
                                </div>
                            </div>

                            <!-- Model Ideal Answer -->
                            <div style="background:var(--bg-card);border-left:3px solid var(--accent-primary);padding:14px;border-radius:4px;margin-bottom:12px;">
                                <strong style="font-size:0.85rem;color:var(--accent-primary);display:block;margin-bottom:4px;">Exemplary Answer Structure:</strong>
                                <p style="font-size:0.875rem;color:var(--text-secondary);line-height:1.6;">${data.sample_answer || 'N/A'}</p>
                            </div>

                            <p style="font-size:0.75rem;color:var(--text-muted);margin-top:10px;">${data.disclaimer}</p>
                        </div>
                    `;
                } else {
                    showToast(data.message || 'Error evaluating answer', 'error');
                }
            } catch (err) {
                showToast('Failed to evaluate answer', 'error');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Submit Answer & Evaluate';
            }
        });
    });
}
