async function loadPackageMeta() {
  const [tokens, mapping] = await Promise.all([
    fetch('../../outputs/qiaomu-editorial-20260418/tokens.json').then(r => r.json()),
    fetch('../../outputs/qiaomu-editorial-20260418/mapping.json').then(r => r.json())
  ]);
  const mount = document.getElementById('packageMeta');
  if (!mount) return;
  mount.innerHTML = `
    <div class="chip chip--accent">${tokens.name}</div>
    <div class="chip">reference: ${new URL(tokens.source_reference_url).hostname}</div>
    <div class="chip">MVP: ${mapping.mvp_order[0]} → ${mapping.mvp_order[mapping.mvp_order.length - 1]}</div>
  `;
}
window.addEventListener('DOMContentLoaded', loadPackageMeta);
