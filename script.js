// JavaScript for the Japanese learning dashboard
function initDashboard() {
  // Copy the global `vocab` array into a local variable.  When served as a
  // static site, `vocab` is defined in static/vocab.js.  The script tags in
  // dashboard.html load `vocab.js` before this script, so `vocab` will be
  // available here.  If the site is extended to use an API, this fallback
  // can be replaced with a fetch call similar to the commented code below.
  let vocabData = typeof vocab !== 'undefined' ? Array.from(vocab) : [];
  const searchInput = document.getElementById('searchInput');
  const cardsContainer = document.getElementById('cardsContainer');
  const categoryButtons = document.querySelectorAll('.category-btn');
  let selectedCategory = 'All';

  // Uncomment the following block if serving data via API
  /*
  fetch('/api/vocab')
    .then((response) => response.json())
    .then((data) => {
      vocabData = data;
      renderCards();
    })
    .catch((err) => {
      console.error('Failed to load vocabulary:', err);
    });
  */

  // Initial render
  renderCards();

  // Event: search input
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      renderCards();
    });
  }

  // Event: category buttons
  categoryButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      categoryButtons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      selectedCategory = btn.dataset.category;
      renderCards();
    });
  });

  // Render cards based on search and selected category
  function renderCards() {
    if (!cardsContainer) return;
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    cardsContainer.innerHTML = '';
    vocabData.forEach((item) => {
      const matchesCategory =
        selectedCategory === 'All' || item.category === selectedCategory;
      const matchesSearch =
        item.word.toLowerCase().includes(query) ||
        item.reading.toLowerCase().includes(query) ||
        item.translation.toLowerCase().includes(query);
      if (matchesCategory && matchesSearch) {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-title">${item.word}</div>
          <div class="card-subtitle">${item.translation}</div>
          <div class="card-category">${item.category}</div>
        `;
        card.addEventListener('click', () => showDetails(item));
        cardsContainer.appendChild(card);
      }
    });
  }

  // Modal elements
  const modal = document.getElementById('detailsModal');
  const closeModalBtn = document.getElementById('closeModal');

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', hideDetails);
  }

  // Show details of a vocabulary item in the modal
  function showDetails(item) {
    const detailWord = document.getElementById('detailWord');
    const detailReading = document.getElementById('detailReading');
    const detailTranslation = document.getElementById('detailTranslation');
    const detailPart = document.getElementById('detailPart');
    const collList = document.getElementById('detailCollocations');
    const detailExample = document.getElementById('detailExample');
    if (detailWord) detailWord.textContent = item.word;
    if (detailReading) detailReading.textContent = item.reading;
    if (detailTranslation) detailTranslation.textContent = item.translation;
    if (detailPart) detailPart.textContent = item.part;
    if (collList) {
      collList.innerHTML = '';
      (item.collocations || []).forEach((coll) => {
        const li = document.createElement('li');
        li.textContent = coll;
        collList.appendChild(li);
      });
    }
    if (detailExample) detailExample.textContent = item.example;
    if (modal) {
      modal.style.display = 'block';
      modal.setAttribute('aria-hidden', 'false');
    }
    // Play audio button
    const playBtn = document.getElementById('playAudio');
    if (playBtn) {
      playBtn.onclick = () => {
        const utterance = new SpeechSynthesisUtterance(item.word);
        utterance.lang = 'ja-JP';
        window.speechSynthesis.speak(utterance);
      };
    }
  }

  // Hide modal
  function hideDetails() {
    if (modal) {
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
    }
    window.speechSynthesis.cancel();
  }

  // Hide modal when clicking outside of the content
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      hideDetails();
    }
  });

  // Expose functions globally if needed
  window.initDashboard = initDashboard;
}

// Run dashboard initialisation on DOMContentLoaded if present
document.addEventListener('DOMContentLoaded', function () {
  if (document.getElementById('cardsContainer')) {
    initDashboard();
  }
});

// Global authentication helpers accessible from HTML
window.isLoggedIn = function () {
  return localStorage.getItem('loggedIn') !== null;
};

window.logoutUser = function () {
  localStorage.removeItem('loggedIn');
  window.location.href = 'index.html';
};