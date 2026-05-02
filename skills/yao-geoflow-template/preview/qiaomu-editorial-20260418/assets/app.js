async function loadPackageMeta() {
  const mount = document.getElementById('packageMeta');
  if (!mount) return;

  try {
    const readJson = async (path) => {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`Unable to load ${path}`);
      }
      return response.json();
    };
    const [tokens, mapping] = await Promise.all([
      readJson('./package/tokens.json'),
      readJson('./package/mapping.json')
    ]);
    const referenceHost = tokens.source_reference_url
      ? new URL(tokens.source_reference_url).hostname
      : 'reference unavailable';
    const routeCount = Array.isArray(mapping.preview_routes)
      ? mapping.preview_routes.length
      : 0;
    mount.innerHTML = `
      <div class="chip chip--accent">${tokens.name}</div>
      <div class="chip">reference: ${referenceHost}</div>
      <div class="chip">MVP: ${mapping.mvp_order[0]} -> ${mapping.mvp_order[mapping.mvp_order.length - 1]}</div>
      <div class="chip">${mapping.coverage_status || 'draft'} / ${mapping.activation_status || 'preview-only'}</div>
      <div class="chip">${routeCount} preview routes</div>
    `;
  } catch (error) {
    mount.innerHTML = '<div class="chip">package metadata unavailable</div>';
  }
}
window.addEventListener('DOMContentLoaded', loadPackageMeta);
