(async () => {
  const container = document.getElementById('services-container');
  if (!container) return;

  try {
    const res = await fetch('https://homeworkflows.mavsankar.com/webhook/services');
    const data = await res.json();
    const services = data.services;

    // Group by category
    const grouped = {};
    services.forEach(s => {
      if (!grouped[s.category]) grouped[s.category] = [];
      grouped[s.category].push(s);
    });

    let html = '';
    for (const [category, items] of Object.entries(grouped)) {
      html += `<h3>${category}</h3>`;
      html += '<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1rem; margin-bottom:1.5rem;">';
      items.forEach(s => {
        const docsLink = s.docs ? `<a href="${s.docs}" target="_blank" rel="noopener" style="font-size:0.85em;">Docs ↗</a>` : '';
        const detailsHtml = s.details ? `<p style="margin:0.5rem 0; color:#ccc; font-size:0.85em;">${s.details}</p>` : '';
        html += `
          <div style="border:1px solid #333; border-radius:8px; padding:1rem; background:#1a1a2e;">
            <strong>${s.name}</strong>
            <p style="margin:0.4rem 0; color:#aaa; font-size:0.9em;">${s.description}</p>
            ${detailsHtml}
            ${docsLink}
          </div>`;
      });
      html += '</div>';
    }

    html += `<p style="color:#666; font-size:0.8em; margin-top:2rem;">Last updated: ${new Date(data.lastUpdated).toLocaleString()}</p>`;
    container.innerHTML = html;
  } catch (e) {
    container.innerHTML = '<p style="color:#cc6666;">Could not load services. The homeserver might be temporarily offline.</p>';
  }
})();
