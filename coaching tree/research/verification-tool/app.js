// State
const app = {
    data: {
        coaches: {},
        relationships: [],
        stints: []
    },
    computed: {
        coachesList: [], // Array version for search/sort
    },
    state: {
        feedbacks: [], // Array of objects containing user feedback
        currentCoachId: null,
        modalContext: null // Stores what exactly is being flagged
    },

    init: async function () {
        await this.loadData();
        this.processData();
        this.renderSidebar();
        this.setupEventListeners();
        this.loadFeedbackState();
    },

    loadData: async function () {
        try {
            // Using standard fetch since this is meant to be served locally
            const [coachesRes, relsRes, stintsRes] = await Promise.all([
                fetch('./data/coaches.json'),
                fetch('./data/relationships.json'),
                fetch('./data/stints.json')
            ]);

            this.data.coaches = await coachesRes.json();
            this.data.relationships = await relsRes.json();
            this.data.stints = await stintsRes.json();
        } catch (error) {
            console.error("Error loading data:", error);
            alert("Could not load data. Ensure you are running a local web server (e.g., using `python3 -m http.server`) from the 'research' folder.");
        }
    },

    processData: function () {
        // Create an array for the sidebar
        this.computed.coachesList = Object.keys(this.data.coaches).map(id => {
            return {
                id: id,
                ...this.data.coaches[id]
            };
        }).sort((a, b) => a.name.localeCompare(b.name));
    },

    // --- RENDERING ---

    renderSidebar: function (searchTerm = '') {
        const listEl = document.getElementById('coach-list');
        listEl.innerHTML = '';

        const term = searchTerm.toLowerCase();
        const filtered = this.computed.coachesList.filter(c =>
            c.name.toLowerCase().includes(term) ||
            (c.hc_schools && c.hc_schools.some(s => s.toLowerCase().includes(term)))
        );

        filtered.forEach(coach => {
            const li = document.createElement('li');
            li.className = `coach-item ${this.state.currentCoachId === coach.id ? 'active' : ''}`;
            li.onclick = () => this.selectCoach(coach.id);

            const schools = coach.hc_schools ? coach.hc_schools.join(', ') : '';
            const desc = schools ? `HC: ${schools}` : (coach.current_status || 'Assistant');

            li.innerHTML = `
                <span class="coach-name">${coach.name}</span>
                <span class="coach-sub">${desc}</span>
            `;
            listEl.appendChild(li);
        });
    },

    selectCoach: function (coachId) {
        this.state.currentCoachId = coachId;
        this.renderSidebar(document.getElementById('coach-search').value);

        const coach = this.data.coaches[coachId];
        this.currentCoach = { id: coachId, ...coach }; // For global access by inline onclicks

        document.getElementById('empty-state').classList.add('hidden');
        document.getElementById('coach-profile').classList.remove('hidden');

        // Profile Header
        document.getElementById('profile-name').textContent = coach.name;
        document.getElementById('profile-status').textContent = coach.current_status || 'Unknown';
        document.getElementById('profile-born').textContent = coach.born ? `${coach.born} ${coach.birthplace ? '(' + coach.birthplace + ')' : ''}` : 'Unknown';
        document.getElementById('profile-alma-mater').textContent = coach.alma_mater || 'Unknown';
        document.getElementById('profile-generation').textContent = coach.generation !== undefined ? coach.generation : 'Unknown';

        this.renderStints(coachId);
        this.renderMentors(coachId);
        this.renderProteges(coachId);
    },

    renderStints: function (coachId) {
        const container = document.getElementById('profile-stints');
        container.innerHTML = '';

        const stints = this.data.stints.filter(s => s.coach_id === coachId)
            .sort((a, b) => (a.year_start || 0) - (b.year_start || 0));

        if (stints.length === 0) {
            container.innerHTML = '<p class="card-sub">No stints recorded.</p>';
            return;
        }

        stints.forEach(stint => {
            const el = document.createElement('div');
            el.className = 'data-card';

            const years = `${stint.year_start || '?'} - ${stint.year_end || '?'}`;
            const role = stint.role.replace('_', ' ').toUpperCase();
            const detail = stint.role_detail ? `(${stint.role_detail})` : '';
            const hcNote = stint.head_coach_id ? `under <strong class="clickable-card" onclick="app.selectCoach('${stint.head_coach_id}')">${this.getCoachName(stint.head_coach_id)}</strong>` : '';

            el.innerHTML = `
                <button class="flag-btn" onclick="app.openFeedbackModal('stint', '${stint.id}')">Flag</button>
                <div class="card-title">${stint.school}</div>
                <div class="card-sub">${years} • ${role} ${detail} ${hcNote}</div>
                ${stint.notes ? `<div class="card-notes">${stint.notes}</div>` : ''}
            `;
            container.appendChild(el);
        });
    },

    renderMentors: function (coachId) {
        const container = document.getElementById('profile-mentors');
        container.innerHTML = '';

        const rels = this.data.relationships.filter(r => r.protege_id === coachId)
            .sort((a, b) => (a.year_start || 0) - (b.year_start || 0));

        if (rels.length === 0) {
            container.innerHTML = '<p class="card-sub">No mentors recorded.</p>';
            return;
        }

        rels.forEach(rel => {
            const el = document.createElement('div');
            el.className = 'data-card clickable-card';

            const years = `${rel.year_start || '?'} - ${rel.year_end || '?'}`;
            const protegeRole = rel.protege_role ? rel.protege_role.replace('_', ' ') : 'assistant';

            el.innerHTML = `
                <button class="flag-btn" onclick="event.stopPropagation(); app.openFeedbackModal('relationship', '${rel.id}')">Flag</button>
                <div class="card-title" onclick="app.selectCoach('${rel.mentor_id}')">${this.getCoachName(rel.mentor_id)}</div>
                <div class="card-sub">${rel.school} (${years}) • as ${protegeRole}</div>
                ${rel.notes ? `<div class="card-notes">${rel.notes}</div>` : ''}
            `;
            container.appendChild(el);
        });
    },

    renderProteges: function (coachId) {
        const container = document.getElementById('profile-proteges');
        container.innerHTML = '';

        const rels = this.data.relationships.filter(r => r.mentor_id === coachId)
            .sort((a, b) => (a.year_start || 0) - (b.year_start || 0));

        if (rels.length === 0) {
            container.innerHTML = '<p class="card-sub">No assistants that became head coaches recorded.</p>';
            return;
        }

        rels.forEach(rel => {
            const el = document.createElement('div');
            el.className = 'data-card clickable-card';

            const years = `${rel.year_start || '?'} - ${rel.year_end || '?'}`;
            const protegeRole = rel.protege_role ? rel.protege_role.replace('_', ' ') : 'assistant';

            el.innerHTML = `
                <button class="flag-btn" onclick="event.stopPropagation(); app.openFeedbackModal('relationship', '${rel.id}')">Flag</button>
                <div class="card-title" onclick="app.selectCoach('${rel.protege_id}')">${this.getCoachName(rel.protege_id)}</div>
                <div class="card-sub">${rel.school} (${years}) • as ${protegeRole}</div>
                ${rel.notes ? `<div class="card-notes">${rel.notes}</div>` : ''}
            `;
            container.appendChild(el);
        });
    },

    getCoachName: function (id) {
        if (!id) return 'Unknown';
        return this.data.coaches[id] ? this.data.coaches[id].name : id;
    },

    // --- FEEDBACK & MODAL LOGIC ---

    setupEventListeners: function () {
        document.getElementById('coach-search').addEventListener('input', (e) => {
            this.renderSidebar(e.target.value);
        });

        document.getElementById('close-modal').addEventListener('click', () => this.closeModal());
        document.getElementById('cancel-modal').addEventListener('click', () => this.closeModal());

        document.getElementById('feedback-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveFeedback();
        });

        document.getElementById('export-feedback-btn').addEventListener('click', () => this.exportFeedback());
        document.getElementById('add-coach-btn').addEventListener('click', () => {
            this.openFeedbackModal('new_coach', 'general');
        });
    },

    openFeedbackModal: function (type, targetId) {
        this.state.modalContext = { type, targetId };

        const modal = document.getElementById('feedback-modal');
        const contextEl = document.getElementById('modal-context');
        const formTitle = document.getElementById('modal-title');

        let ctxText = "";

        if (type === 'coach') {
            formTitle.textContent = "Flag Coach Info";
            ctxText = `You are flagging info for coach: <strong>${this.getCoachName(targetId)}</strong>.`;
        } else if (type === 'relationship') {
            formTitle.textContent = "Flag Relationship";
            const rel = this.data.relationships.find(r => r.id === targetId);
            ctxText = `Flagging relationship: <strong>${this.getCoachName(rel.mentor_id)}</strong> -> <strong>${this.getCoachName(rel.protege_id)}</strong> at ${rel.school}.`;
        } else if (type === 'stint') {
            formTitle.textContent = "Flag Stint";
            const stint = this.data.stints.find(s => s.id === targetId);
            ctxText = `Flagging stint: <strong>${this.getCoachName(stint.coach_id)}</strong> at ${stint.school}.`;
        } else if (type === 'new_coach') {
            formTitle.textContent = "Suggest Missing Coach";
            ctxText = "Please provide details about the missing coach so researchers can add them to the database.";
        } else if (type === 'new_stint' || type === 'new_mentor' || type === 'new_protege') {
            formTitle.textContent = "Add Missing Connection";
            ctxText = `You are suggesting a new connection for: <strong>${this.getCoachName(targetId)}</strong>.`;
        }

        contextEl.innerHTML = ctxText;
        document.getElementById('feedback-notes').value = '';
        modal.classList.remove('hidden');
    },

    closeModal: function () {
        document.getElementById('feedback-modal').classList.add('hidden');
        this.state.modalContext = null;
    },

    saveFeedback: function () {
        if (!this.state.modalContext) return;

        const type = document.getElementById('feedback-type').value;
        const notes = document.getElementById('feedback-notes').value;

        const feedback = {
            id: 'fb-' + Date.now(),
            timestamp: new Date().toISOString(),
            context: this.state.modalContext,
            issueType: type,
            notes: notes
        };

        this.state.feedbacks.push(feedback);
        this.persistFeedbackState();
        this.updateFeedbackBadge();

        this.closeModal();
        alert("Feedback saved! Don't forget to export your feedback when you are done.");
    },

    loadFeedbackState: function () {
        try {
            const saved = localStorage.getItem('coachingTreeFeedback');
            if (saved) {
                this.state.feedbacks = JSON.parse(saved);
                this.updateFeedbackBadge();
            }
        } catch (e) { }
    },

    persistFeedbackState: function () {
        try {
            localStorage.setItem('coachingTreeFeedback', JSON.stringify(this.state.feedbacks));
        } catch (e) { }
    },

    updateFeedbackBadge: function () {
        const badge = document.getElementById('feedback-badge');
        badge.textContent = this.state.feedbacks.length;
        if (this.state.feedbacks.length > 0) {
            badge.style.background = '#fef08a'; // yellow to highlight
            badge.style.color = '#854d0e';
        }
    },

    exportFeedback: function () {
        if (this.state.feedbacks.length === 0) {
            alert("You have no feedback items to export yet.");
            return;
        }

        const dataStr = JSON.stringify(this.state.feedbacks, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

        const exportFileDefaultName = 'coaching_tree_feedback_' + new Date().toISOString().slice(0, 10) + '.json';

        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();

        if (confirm("Feedback downloaded. Would you like to clear your feedback history now?")) {
            this.state.feedbacks = [];
            this.persistFeedbackState();
            this.updateFeedbackBadge();
        }
    }
};

// Start
document.addEventListener('DOMContentLoaded', () => app.init());
