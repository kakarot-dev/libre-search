<script>
  import SearchBar from './components/SearchBar.svelte';
  import SearchResults from './components/SearchResults.svelte';
  import UploadPanel from './components/UploadPanel.svelte';
  import DocumentList from './components/DocumentList.svelte';
  import DocViewer from './components/DocViewer.svelte';

  let results = $state(null);
  let overlay = $state(null);
  let searched = $state(false);
  let query = $state('');
  let viewer = $state(null); // { docId, filename, chunkIndex }

  function handleResults(data) {
    results = data;
    searched = true;
  }

  function goHome() {
    searched = false;
    results = null;
  }

  function openOverlay(type) {
    overlay = overlay === type ? null : type;
  }

  function closeOverlay() {
    overlay = null;
  }

  function openViewer(result) {
    viewer = {
      docId: result.document_id,
      filename: result.filename,
      chunkIndex: result.chunk_index,
    };
  }

  function closeViewer() {
    viewer = null;
  }
</script>

{#if searched}
  <!-- ===== RESULTS MODE (Google-style) ===== -->
  <div class="results-page">
    <header class="top-bar">
      <button class="top-brand" onclick={goHome}>
        <span class="top-icon">&#x2B22;</span>
        <span class="top-name">LibreSearch</span>
      </button>
      <div class="top-search">
        <SearchBar onresults={handleResults} bind:query compact />
      </div>
    </header>

    <main class="results-body">
      <SearchResults {results} onopen={openViewer} />
    </main>
  </div>
{:else}
  <!-- ===== HOME MODE (Google-style landing) ===== -->
  <div class="home-page">
    <div class="ambient"></div>
    <div class="home-center">
      <div class="brand">
        <span class="brand-icon">&#x2B22;</span>
        <h1>LibreSearch</h1>
        <p class="tagline">semantic intelligence</p>
      </div>
      <SearchBar onresults={handleResults} bind:query />
    </div>
  </div>
{/if}

<!-- Floating sidebar icons (always visible) -->
<div class="sidebar">
  <button
    class="sidebar-btn"
    class:active={overlay === 'upload'}
    onclick={() => openOverlay('upload')}
    aria-label="Upload documents"
  >
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" y1="3" x2="12" y2="15" />
    </svg>
    <span class="sidebar-label">Upload</span>
  </button>

  <button
    class="sidebar-btn"
    class:active={overlay === 'documents'}
    onclick={() => openOverlay('documents')}
    aria-label="View documents"
  >
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <polyline points="10 9 9 9 8 9" />
    </svg>
    <span class="sidebar-label">Library</span>
  </button>
</div>

<!-- Overlay panels -->
{#if overlay}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div class="overlay-backdrop" onclick={closeOverlay}></div>
  <div class="overlay-panel">
    <div class="overlay-header">
      <h2>{overlay === 'upload' ? 'Upload Document' : 'Document Library'}</h2>
      <button class="overlay-close" onclick={closeOverlay} aria-label="Close panel">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>
    </div>
    {#if overlay === 'upload'}
      <UploadPanel />
    {:else}
      <DocumentList />
    {/if}
  </div>
{/if}

<!-- Document viewer popup -->
{#if viewer}
  <DocViewer
    docId={viewer.docId}
    filename={viewer.filename}
    highlightChunk={viewer.chunkIndex}
    onclose={closeViewer}
  />
{/if}

<style>
  /* ===== HOME PAGE ===== */
  .home-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .ambient {
    position: fixed;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse, #00ffc808 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .home-center {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 620px;
    padding: 0 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: -8vh;
  }

  .brand {
    text-align: center;
    margin-bottom: 2.5rem;
    user-select: none;
  }

  .brand-icon {
    font-size: 2rem;
    color: var(--neon);
    filter: drop-shadow(0 0 12px #00ffc840);
    display: block;
    margin-bottom: 0.75rem;
    animation: pulse-glow 4s ease-in-out infinite;
  }

  @keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 12px #00ffc840); }
    50% { filter: drop-shadow(0 0 24px #00ffc860); }
  }

  h1 {
    font-family: var(--font);
    font-size: 2.2rem;
    font-weight: 300;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--text);
  }

  .tagline {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-top: 0.4rem;
  }

  /* ===== RESULTS PAGE ===== */
  .results-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .top-bar {
    position: sticky;
    top: 0;
    z-index: 50;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1.1rem 2rem;
    background: var(--black-1);
    border-bottom: 1px solid var(--black-3);
  }

  .top-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    flex-shrink: 0;
    transition: opacity 0.15s;
  }

  .top-brand:hover {
    opacity: 0.7;
  }

  .top-icon {
    font-size: 1.1rem;
    color: var(--neon);
    filter: drop-shadow(0 0 8px #00ffc840);
  }

  .top-name {
    font-family: var(--font);
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .top-search {
    flex: 1;
    max-width: 560px;
  }

  .results-body {
    padding: 1.5rem 1.5rem 3rem;
    max-width: 760px;
    width: 100%;
    margin-left: 180px;
  }

  @media (max-width: 1024px) {
    .results-body {
      margin-left: auto;
      margin-right: auto;
    }
  }

  /* ===== SIDEBAR ===== */
  .sidebar {
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .sidebar-btn {
    position: relative;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    background: var(--black-2);
    border-right: 2px solid transparent;
    border-radius: 8px 0 0 8px;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: visible;
  }

  .sidebar-btn svg {
    width: 20px;
    height: 20px;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    flex-shrink: 0;
  }

  .sidebar-label {
    position: absolute;
    right: calc(100% + 10px);
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--neon);
    white-space: nowrap;
    opacity: 0;
    transform: translateX(8px);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: none;
  }

  .sidebar-btn:hover {
    width: 56px;
    height: 56px;
    color: var(--neon);
    background: var(--black-3);
    border-right-color: var(--neon);
    box-shadow: inset 0 0 20px #00ffc808, -4px 0 20px #00ffc810;
  }

  .sidebar-btn:hover svg {
    width: 24px;
    height: 24px;
    filter: drop-shadow(0 0 6px #00ffc860);
  }

  .sidebar-btn:hover .sidebar-label {
    opacity: 1;
    transform: translateX(0);
  }

  .sidebar-btn.active {
    width: 56px;
    height: 56px;
    color: var(--neon);
    background: var(--black-3);
    border-right-color: var(--neon);
  }

  .sidebar-btn.active svg {
    width: 24px;
    height: 24px;
  }

  /* ===== OVERLAY ===== */
  .overlay-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    z-index: 200;
    animation: fade-in 0.25s ease;
  }

  .overlay-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 201;
    width: 90%;
    max-width: 580px;
    max-height: 80vh;
    overflow-y: auto;
    background: var(--black-2);
    border: 1px solid var(--black-4);
    border-radius: 16px;
    padding: 2rem;
    animation: scale-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .overlay-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .overlay-header h2 {
    font-family: var(--mono);
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--neon);
  }

  .overlay-close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    border-radius: 6px;
    transition: all 0.15s;
  }

  .overlay-close svg {
    width: 16px;
    height: 16px;
  }

  .overlay-close:hover {
    color: var(--text);
    background: var(--black-4);
  }

  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes scale-in {
    from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  }
</style>
