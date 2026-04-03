<script>
  import { getDocuments, deleteDocument } from '../lib/api.js';
  import { untrack } from 'svelte';

  let documents = $state([]);
  let loading = $state(true);
  let error = $state('');

  async function load() {
    loading = true;
    error = '';
    try {
      documents = await getDocuments();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function handleDelete(docId) {
    try {
      await deleteDocument(docId);
      documents = documents.filter((d) => d.id !== docId);
    } catch (e) {
      error = e.message;
    }
  }

  function formatDate(iso) {
    return new Date(iso).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  $effect(() => {
    untrack(() => load());
  });
</script>

<div class="docs">
  {#if loading}
    <div class="state">
      <span class="spinner"></span>
    </div>
  {:else if error}
    <p class="state error">{error}</p>
  {:else if documents.length === 0}
    <div class="state">
      <p>No documents yet</p>
    </div>
  {:else}
    <div class="list">
      {#each documents as doc (doc.id)}
        <div class="doc-row">
          <div class="doc-info">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <div class="doc-meta">
              <span class="doc-name">{doc.filename}</span>
              <span class="doc-detail">
                {doc.num_chunks} chunks &middot; {formatDate(doc.created_at)}
              </span>
            </div>
          </div>
          <button class="delete-btn" onclick={() => handleDelete(doc.id)} aria-label="Delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            </svg>
          </button>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .docs {
    width: 100%;
  }

  .state {
    text-align: center;
    padding: 2rem 0;
    color: var(--text-dim);
    font-size: 0.8rem;
    font-weight: 300;
    display: flex;
    justify-content: center;
  }

  .state.error {
    color: var(--danger);
  }

  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid var(--black-4);
    border-top-color: var(--neon);
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .doc-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0.75rem;
    border-radius: 8px;
    transition: background 0.15s;
  }

  .doc-row:hover {
    background: var(--black-3);
  }

  .doc-info {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    min-width: 0;
  }

  .doc-info > svg {
    width: 16px;
    height: 16px;
    color: var(--text-dim);
    flex-shrink: 0;
  }

  .doc-meta {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .doc-name {
    font-size: 0.8rem;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .doc-detail {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--text-dim);
    margin-top: 0.15rem;
  }

  .delete-btn {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-dim);
    border-radius: 6px;
    flex-shrink: 0;
    transition: all 0.15s;
    opacity: 0;
  }

  .doc-row:hover .delete-btn {
    opacity: 1;
  }

  .delete-btn svg {
    width: 14px;
    height: 14px;
  }

  .delete-btn:hover {
    color: var(--danger);
    background: #ff3b3b10;
  }
</style>
