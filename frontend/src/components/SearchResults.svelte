<script>
  import ResultCard from './ResultCard.svelte';

  let { results = null, onopen = () => {} } = $props();
</script>

{#if results}
  <div class="results">
    {#if results.total > 0}
      <p class="meta">
        About <span class="count">{results.total}</span> results for
        <span class="query">"{results.query}"</span>
      </p>
      <div class="list">
        {#each results.results as result, i (result.chunk_id)}
          <ResultCard {result} index={i} onclick={onopen} />
        {/each}
      </div>
    {:else}
      <div class="empty">
        <p class="empty-main">No results found for <span>"{results.query}"</span></p>
        <p class="empty-hint">Try different keywords or upload more documents</p>
      </div>
    {/if}
  </div>
{/if}

<style>
  .results {
    width: 100%;
    animation: fade-in 0.2s ease;
  }

  @keyframes fade-in {
    from { opacity: 0; }
  }

  .meta {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--black-3);
  }

  .count {
    color: var(--text);
    font-weight: 500;
  }

  .query {
    color: var(--text);
  }

  .list {
    display: flex;
    flex-direction: column;
  }

  .empty {
    padding: 3rem 0;
  }

  .empty-main {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
  }

  .empty-main span {
    color: var(--text);
    font-weight: 500;
  }

  .empty-hint {
    font-size: 0.8rem;
    color: var(--text-dim);
  }
</style>
