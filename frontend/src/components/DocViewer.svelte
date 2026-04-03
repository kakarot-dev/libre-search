<script>
  import { getDocumentChunks } from '../lib/api.js';
  import { untrack } from 'svelte';

  let { docId = '', filename = '', highlightChunk = 0, onclose = () => {} } = $props();

  let chunks = $state([]);
  let loading = $state(true);
  let error = $state('');

  $effect(() => {
    untrack(() => loadChunks());
  });

  async function loadChunks() {
    if (!docId) return;
    loading = true;
    error = '';
    try {
      chunks = await getDocumentChunks(docId);
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
      // Scroll to highlighted chunk after render
      setTimeout(scrollToHighlight, 100);
    }
  }

  function scrollToHighlight() {
    const el = document.getElementById(`chunk-${highlightChunk}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div class="viewer-backdrop" onclick={onclose}></div>
<div class="viewer-panel">
  <div class="viewer-header">
    <div class="viewer-title">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
      </svg>
      <span class="viewer-filename">{filename}</span>
      <span class="viewer-count">{chunks.length} chunks</span>
    </div>
    <button class="viewer-close" onclick={onclose} aria-label="Close viewer">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </button>
  </div>

  <div class="viewer-body">
    {#if loading}
      <div class="viewer-state">
        <span class="spinner"></span>
      </div>
    {:else if error}
      <p class="viewer-state viewer-error">{error}</p>
    {:else}
      {#each chunks as chunk (chunk.chunk_index)}
        <div
          id="chunk-{chunk.chunk_index}"
          class="chunk-block"
          class:highlighted={chunk.chunk_index === highlightChunk}
        >
          <span class="chunk-num">#{chunk.chunk_index}</span>
          <p class="chunk-text">{chunk.text}</p>
        </div>
      {/each}
    {/if}
  </div>
</div>

<style>
  .viewer-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(6px);
    z-index: 300;
    animation: fade-in 0.2s ease;
  }

  @keyframes fade-in {
    from { opacity: 0; }
  }

  .viewer-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 301;
    width: 92%;
    max-width: 720px;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    background: var(--black-1);
    border: 1px solid var(--black-4);
    border-radius: 16px;
    animation: scale-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
  }

  @keyframes scale-in {
    from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  }

  .viewer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--black-3);
    flex-shrink: 0;
  }

  .viewer-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 0;
  }

  .viewer-title svg {
    width: 16px;
    height: 16px;
    color: var(--neon);
    flex-shrink: 0;
  }

  .viewer-filename {
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .viewer-count {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--text-dim);
    background: var(--black-3);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    flex-shrink: 0;
  }

  .viewer-close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    border-radius: 6px;
    transition: all 0.15s;
    flex-shrink: 0;
  }

  .viewer-close svg {
    width: 16px;
    height: 16px;
  }

  .viewer-close:hover {
    color: var(--text);
    background: var(--black-4);
  }

  .viewer-body {
    overflow-y: auto;
    padding: 1rem 1.5rem 2rem;
    flex: 1;
  }

  .viewer-state {
    text-align: center;
    padding: 3rem 0;
    color: var(--text-dim);
    display: flex;
    justify-content: center;
  }

  .viewer-error {
    color: var(--danger);
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid var(--black-4);
    border-top-color: var(--neon);
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* Chunks */
  .chunk-block {
    position: relative;
    padding: 0.75rem 0.75rem 0.75rem 2.5rem;
    margin-bottom: 0.25rem;
    border-radius: 6px;
    border-left: 2px solid transparent;
    transition: all 0.2s;
  }

  .chunk-block.highlighted {
    background: #00ffc808;
    border-left-color: var(--neon);
    box-shadow: inset 0 0 30px #00ffc806;
  }

  .chunk-num {
    position: absolute;
    left: 0.5rem;
    top: 0.8rem;
    font-family: var(--mono);
    font-size: 0.55rem;
    color: var(--text-dim);
    user-select: none;
  }

  .highlighted .chunk-num {
    color: var(--neon);
  }

  .chunk-text {
    font-size: 0.82rem;
    line-height: 1.7;
    color: var(--text-muted);
    font-weight: 300;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .highlighted .chunk-text {
    color: var(--text);
  }
</style>
