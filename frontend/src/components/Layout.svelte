<script>
  let { activeTab = $bindable('search'), children } = $props();

  const tabs = [
    { id: 'search', label: 'Search' },
    { id: 'upload', label: 'Upload' },
    { id: 'documents', label: 'Documents' },
  ];
</script>

<div class="app">
  <header>
    <h1>Semantic Search Engine</h1>
    <nav>
      {#each tabs as tab}
        <button
          class="tab"
          class:active={activeTab === tab.id}
          onclick={() => (activeTab = tab.id)}
        >
          {tab.label}
        </button>
      {/each}
    </nav>
  </header>

  <main>
    {@render children()}
  </main>
</div>

<style>
  .app {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  header {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-text);
  }

  nav {
    display: flex;
    gap: 0.5rem;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 0.5rem;
  }

  .tab {
    padding: 0.5rem 1rem;
    border: none;
    background: none;
    color: var(--color-text-muted);
    font-size: 0.9rem;
    border-radius: var(--radius);
    transition: all 0.15s;
  }

  .tab:hover {
    color: var(--color-text);
    background: var(--color-surface);
  }

  .tab.active {
    color: var(--color-primary);
    background: var(--color-surface);
    font-weight: 500;
  }

  main {
    min-height: 400px;
  }
</style>
