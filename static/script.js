document.getElementById('matchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const submitButton = e.target.querySelector('button[type="submit"]');
    
    try {
        submitButton.disabled = true;
        submitButton.innerHTML = 'Analyzing...';
        
        const response = await fetch('/match', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        console.log('Response data:', data);  // Debug log
        
        if (response.ok) {
            displayResults(data);
        } else {
            console.error('Error response:', data);  // Debug log
            alert(data.error || 'An error occurred while processing the resume');
        }
    } catch (error) {
        console.error('Request error:', error);  // Debug log
        alert('An error occurred while processing the request');
        console.error(error);
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Analyze Match';
    }
});

function displayResults(data) {
    console.log('Displaying results:', data);  // Debug log
    const resultsDiv = document.getElementById('results');
    resultsDiv.classList.remove('d-none');
    
    // Update match score
    const progressBar = resultsDiv.querySelector('.progress-bar');
    const scoreValue = resultsDiv.querySelector('.score-value');
    progressBar.style.width = `${data.match_score}%`;
    scoreValue.textContent = `${data.match_score}%`;
    
    // Update matching skills
    const matchingSkillsList = resultsDiv.querySelector('.matching-skills .skills-list');
    console.log('Matching skills:', data.matching_skills);  // Debug log
    matchingSkillsList.innerHTML = data.matching_skills
        .map(skill => `<span class="skill-tag">${skill}</span>`)
        .join('');
    
    // Update missing skills
    const missingSkillsList = resultsDiv.querySelector('.missing-skills .skills-list');
    console.log('Missing skills:', data.missing_skills);  // Debug log
    missingSkillsList.innerHTML = data.missing_skills
        .map(skill => `<span class="skill-tag">${skill}</span>`)
        .join('');
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}
