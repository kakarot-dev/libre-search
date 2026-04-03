<script>
  let { result, index = 0, onclick = () => {} } = $props();

  function formatScore(score) {
    return (score * 100).toFixed(1);
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div class="card" style="animation-delay: {index * 50}ms" onclick={() => onclick(result)}>
  <!-- Source URL line -->
  <div class="source-line">
    <span class="source-name">{result.filename}</span>
    <span class="source-sep">&rsaquo;</span>
    <span class="source-chunk">chunk {result.chunk_index}</span>
    <span class="relevance">{formatScore(result.similarity)}% match</span>
  </div>

  <!-- Snippet text -->
  <p class="snippet">{result.text}</p>

  <!-- Badges row -->
  <div class="badges">
    <span class="badge">KNN: cosine</span>
    <span class="badge">HNSW index</span>
    <span class="badge">gemma-emb</span>
    <span class="badge">dim: 768</span>
  </div>
</div>

<style>
  .card {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid var(--black-3);
    animation: slide-up 0.35s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.15s;
  }

  .card:hover {
    background: var(--black-2);
  }

  @keyframes slide-up {
    from { opacity: 0; transform: translateY(8px); }
  }

  /* Source */
  .source-line {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
  }

  .source-name {
    font-size: 0.8rem;
    color: var(--neon);
    opacity: 0.8;
  }

  .source-sep {
    color: var(--text-dim);
    font-size: 0.7rem;
  }

  .source-chunk {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-dim);
  }

  .relevance {
    margin-left: auto;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 500;
    color: var(--neon);
    background: #00ffc808;
    border: 1px solid #00ffc820;
    padding: 0.1rem 0.45rem;
    border-radius: 4px;
  }

  /* Snippet */
  .snippet {
    font-size: 0.88rem;
    line-height: 1.7;
    color: var(--text);
    font-weight: 300;
    white-space: pre-wrap;
    word-break: break-word;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 0.65rem;
  }

  /* Badges */
  .badges {
    display: flex;
    gap: 0.3rem;
    flex-wrap: wrap;
  }

  .badge {
    font-family: var(--mono);
    font-size: 0.55rem;
    letter-spacing: 0.03em;
    color: var(--neon);
    background: #00ffc806;
    border: 1px solid #00ffc818;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }
</style>
