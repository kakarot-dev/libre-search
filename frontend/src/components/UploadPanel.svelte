<script>
  import { uploadDocument } from '../lib/api.js';

  let loading = $state(false);
  let message = $state('');
  let error = $state('');
  let dragover = $state(false);
  let progress = $state('');

  let done = $state(false);

  async function handleFile(file) {
    if (!file) return;
    loading = true;
    message = '';
    error = '';
    done = false;
    progress = 'Parsing & chunking...';
    try {
      progress = 'Embedding chunks...';
      const data = await uploadDocument(file);
      message = data.message;
      done = true;
    } catch (e) {
      error = e.message;
      done = true;
    } finally {
      loading = false;
      progress = '';
    }
  }

  function reset() {
    done = false;
    message = '';
    error = '';
  }

  function handleInput(e) {
    handleFile(e.target.files[0]);
  }

  function handleDrop(e) {
    e.preventDefault();
    dragover = false;
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }

  function handleDragOver(e) {
    e.preventDefault();
    dragover = true;
  }

  function handleDragLeave() {
    dragover = false;
  }
</script>

{#if done}
  <div class="result-state" class:has-error={!!error}>
    {#if message}
      <svg class="result-icon success-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
      <p class="result-text">{message}</p>
    {:else}
      <svg class="result-icon error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="15" y1="9" x2="9" y2="15" />
        <line x1="9" y1="9" x2="15" y2="15" />
      </svg>
      <p class="result-text error-text">{error}</p>
    {/if}
    <button class="upload-again" onclick={reset}>Upload another</button>
  </div>
{:else}
  <div
    class="drop-zone"
    class:dragover
    class:loading
    ondrop={handleDrop}
    ondragover={handleDragOver}
    ondragleave={handleDragLeave}
    role="button"
    tabindex="0"
  >
    {#if loading}
      <div class="loader">
        <span class="spinner"></span>
        <p class="loader-text">{progress}</p>
      </div>
    {:else}
      <svg class="drop-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="17 8 12 3 7 8" />
        <line x1="12" y1="3" x2="12" y2="15" />
      </svg>
      <p class="drop-label">Drop file or click to browse</p>
      <p class="drop-hint">PDF, DOCX, TXT, MD, CSV, HTML, JSON</p>
      <input
        type="file"
        onchange={handleInput}
        accept=".pdf,.docx,.txt,.md,.csv,.log,.json,.xml,.html"
      />
    {/if}
  </div>
{/if}

<style>
  .drop-zone {
    position: relative;
    border: 1px dashed var(--black-4);
    border-radius: var(--radius);
    padding: 2.5rem 2rem;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    background: var(--black-1);
  }

  .drop-zone:hover,
  .drop-zone.dragover {
    border-color: var(--neon);
    background: #00ffc805;
    box-shadow: inset 0 0 40px #00ffc805;
  }

  .drop-zone.loading {
    cursor: wait;
    border-style: solid;
    border-color: var(--neon-dim);
  }

  .drop-icon {
    width: 28px;
    height: 28px;
    color: var(--text-dim);
    margin-bottom: 0.75rem;
    transition: color 0.2s;
  }

  .drop-zone:hover .drop-icon {
    color: var(--neon);
  }

  .drop-label {
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
  }

  .drop-hint {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--text-dim);
    letter-spacing: 0.05em;
  }

  input[type='file'] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
  }

  .loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
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

  .loader-text {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-dim);
  }

  .result-state {
    text-align: center;
    padding: 2rem 1rem;
    animation: fade-in 0.3s ease;
  }

  @keyframes fade-in {
    from { opacity: 0; }
  }

  .result-icon {
    width: 36px;
    height: 36px;
    margin-bottom: 1rem;
  }

  .success-icon {
    color: var(--neon);
    filter: drop-shadow(0 0 10px #00ffc840);
  }

  .error-icon {
    color: var(--danger);
  }

  .result-text {
    font-size: 0.85rem;
    color: var(--text);
    line-height: 1.5;
    margin-bottom: 1.25rem;
  }

  .error-text {
    color: var(--danger);
  }

  .upload-again {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    padding: 0.5rem 1rem;
    border: 1px solid var(--black-4);
    border-radius: 6px;
    background: var(--black-3);
    cursor: pointer;
    transition: all 0.15s;
  }

  .upload-again:hover {
    color: var(--neon);
    border-color: var(--neon-dim);
  }
</style>
