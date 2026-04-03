<script>
  import { searchDocuments } from '../lib/api.js';

  let { onresults = () => {}, compact = false, query = $bindable('') } = $props();
  let topK = $state(10);
  let loading = $state(false);
  let error = $state('');
  let focused = $state(false);
  let suggestions = $state([]);
  let showSuggestions = $state(false);
  let selectedIdx = $state(-1);
  let debounceTimer;

  async function handleSearch(q) {
    const term = (q ?? query).trim();
    if (!term) return;
    query = term;
    showSuggestions = false;
    loading = true;
    error = '';
    try {
      const data = await searchDocuments(term, topK);
      onresults(data);
      addRecent(term);
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') {
      if (selectedIdx >= 0 && selectedIdx < suggestions.length) {
        query = suggestions[selectedIdx];
      }
      handleSearch();
      selectedIdx = -1;
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIdx = Math.min(selectedIdx + 1, suggestions.length - 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIdx = Math.max(selectedIdx - 1, -1);
    } else if (e.key === 'Escape') {
      showSuggestions = false;
    }
  }

  function handleTyping() {
    clearTimeout(debounceTimer);
    selectedIdx = -1;
    if (query.trim().length >= 1) {
      debounceTimer = setTimeout(buildSuggestions, 150);
    } else {
      showSuggestions = false;
    }
  }

  function buildSuggestions() {
    const term = query.trim().toLowerCase();
    if (!term) { showSuggestions = false; return; }
    const recents = getRecents();
    const patterns = [
      `${query.trim()} definition`,
      `${query.trim()} example`,
      `what is ${query.trim()}`,
      `how does ${query.trim()} work`,
    ];
    const matched = recents.filter(r => r.toLowerCase().includes(term) && r.toLowerCase() !== term);
    const all = [...matched, ...patterns];
    suggestions = [...new Set(all)].slice(0, 5);
    showSuggestions = suggestions.length > 0 && focused;
  }

  function pickSuggestion(s) {
    query = s;
    showSuggestions = false;
    handleSearch(s);
  }

  function handleFocus() {
    focused = true;
    if (query.trim().length >= 1) buildSuggestions();
  }

  function handleBlur() {
    // Delay so click on suggestion registers
    setTimeout(() => { focused = false; showSuggestions = false; }, 200);
  }

  function getRecents() {
    try { return JSON.parse(localStorage.getItem('ls_recents') || '[]'); }
    catch { return []; }
  }

  function addRecent(term) {
    const recents = getRecents().filter(r => r !== term);
    recents.unshift(term);
    localStorage.setItem('ls_recents', JSON.stringify(recents.slice(0, 10)));
  }
</script>

<div class="search-wrap" class:focused class:loading class:compact>
  <div class="search-box" class:has-dropdown={showSuggestions}>
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
      <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
    <input
      type="text"
      bind:value={query}
      onkeydown={handleKeydown}
      oninput={handleTyping}
      onfocus={handleFocus}
      onblur={handleBlur}
      placeholder="Ask anything..."
      disabled={loading}
    />
    {#if !compact}
      <select bind:value={topK}>
        <option value={5}>5</option>
        <option value={10}>10</option>
        <option value={20}>20</option>
      </select>
    {/if}
    <button class="go-btn" onclick={() => handleSearch()} disabled={loading || !query.trim()}>
      {#if loading}
        <span class="spinner"></span>
      {:else}
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
        </svg>
      {/if}
    </button>
  </div>

  {#if showSuggestions}
    <div class="dropdown">
      {#each suggestions as s, i}
        <button
          class="dropdown-item"
          class:selected={i === selectedIdx}
          onmousedown={() => pickSuggestion(s)}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <span>{s}</span>
        </button>
      {/each}
    </div>
  {/if}

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>

<style>
  .search-wrap {
    width: 100%;
    position: relative;
  }

  .search-wrap:not(.compact) {
    margin-bottom: 2rem;
  }

  .search-box {
    display: flex;
    align-items: center;
    gap: 0;
    background: var(--black-2);
    border: 1px solid var(--black-4);
    border-radius: 999px;
    padding: 0.25rem 0.25rem 0.25rem 1.25rem;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .search-box.has-dropdown {
    border-radius: 20px 20px 0 0;
  }

  .compact .search-box {
    background: var(--black-2);
    border-color: var(--black-3);
    padding: 0.15rem 0.15rem 0.15rem 1rem;
  }

  .focused .search-box {
    border-color: var(--neon);
    box-shadow: var(--neon-glow);
  }

  .focused .search-box.has-dropdown {
    box-shadow: 0 0 20px #00ffc815;
    border-bottom-color: var(--black-3);
  }

  .search-icon {
    width: 18px;
    height: 18px;
    color: var(--text-dim);
    flex-shrink: 0;
    transition: color 0.2s;
  }

  .compact .search-icon { width: 16px; height: 16px; }
  .focused .search-icon { color: var(--neon); }

  input {
    flex: 1;
    padding: 0.8rem 0.75rem;
    background: none;
    border: none;
    color: var(--text);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 0.02em;
  }

  .compact input { padding: 0.55rem 0.75rem; font-size: 0.9rem; }
  input::placeholder { color: var(--text-dim); font-weight: 300; }

  select {
    padding: 0.4rem 0.5rem;
    background: var(--black-3);
    border: 1px solid var(--black-4);
    border-radius: 6px;
    color: var(--text-muted);
    font-size: 0.7rem;
    font-family: var(--mono);
    cursor: pointer;
    transition: border-color 0.15s;
  }

  select:hover { border-color: var(--text-dim); }

  .go-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--black-3);
    color: var(--text-muted);
    margin-left: 0.5rem;
    flex-shrink: 0;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .compact .go-btn { width: 34px; height: 34px; }
  .go-btn svg { width: 16px; height: 16px; }
  .compact .go-btn svg { width: 14px; height: 14px; }

  .go-btn:hover:not(:disabled) {
    background: var(--neon);
    color: var(--black);
    box-shadow: 0 0 16px #00ffc840;
    transform: scale(1.05);
  }

  .go-btn:disabled { opacity: 0.3; cursor: not-allowed; }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid var(--text-dim);
    border-top-color: var(--neon);
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* Dropdown */
  .dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    z-index: 50;
    background: var(--black-2);
    border: 1px solid var(--neon);
    border-top: none;
    border-radius: 0 0 16px 16px;
    overflow: hidden;
    animation: drop-in 0.15s ease;
  }

  @keyframes drop-in {
    from { opacity: 0; transform: translateY(-4px); }
  }

  .dropdown-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.6rem 1.25rem;
    color: var(--text-muted);
    font-size: 0.85rem;
    font-weight: 300;
    text-align: left;
    transition: background 0.1s;
  }

  .dropdown-item svg {
    width: 14px;
    height: 14px;
    color: var(--text-dim);
    flex-shrink: 0;
  }

  .dropdown-item:hover,
  .dropdown-item.selected {
    background: var(--black-3);
    color: var(--text);
  }

  .error {
    margin-top: 0.75rem;
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--danger);
    text-align: center;
  }
</style>
