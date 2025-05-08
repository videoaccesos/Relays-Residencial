// static/js/remote.js

document.addEventListener('DOMContentLoaded', () => {
  const panel = document.getElementById('relay-panel');

  fetch('/api/residences?page=1', { credentials: 'same-origin' })
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(residences => {
      if (!residences.length) {
        panel.innerHTML = '<p>No hay residencias.</p>';
        return;
      }
      const sel = document.createElement('select');
      sel.className = 'form-control mb-3';
      residences.forEach(r => {
        const o = document.createElement('option');
        o.value = r.id; o.text = r.name;
        sel.appendChild(o);
      });
      sel.onchange = () => loadRelays(sel.value);
      panel.appendChild(sel);
      loadRelays(residences[0].id);
    })
    .catch(err => {
      panel.innerHTML = `<div class="alert alert-danger">Error: ${err}</div>`;
    });
});


function loadRelays(resId) {
  const panel = document.getElementById('relay-panel');
  const sel   = panel.querySelector('select');
  panel.innerHTML = '';
  panel.appendChild(sel);

  fetch(`/api/residences/${resId}/relays`, { credentials: 'same-origin' })
    .then(r => r.ok ? r.json() : r.text().then(t=>Promise.reject(t)))
    .then(relays => {
      const row = document.createElement('div');
      row.className = 'row';
      relays.forEach(r => {
        const col  = document.createElement('div');
        col.className = 'col-3 mb-3';
        const card = document.createElement('div');
        card.className = 'card p-2 text-center';

        const title = document.createElement('h5');
        title.innerText = r.name;

        const onBtn = document.createElement('button');
        onBtn.className = 'btn btn-success btn-block';
        onBtn.innerText = 'Abrir';
        onBtn.onclick = () => execute(resId, r.relay_id, 2);

        const offBtn = document.createElement('button');
        offBtn.className = 'btn btn-danger btn-block mt-1';
        offBtn.innerText = 'Cerrar';
        offBtn.onclick = () => execute(resId, r.relay_id, 0);

        card.append(title, onBtn, offBtn);
        col.appendChild(card);
        row.appendChild(col);
      });
      panel.appendChild(row);
    })
    .catch(err => {
      panel.insertAdjacentHTML(
        'beforeend',
        `<div class="alert alert-danger mt-3"><pre>${err}</pre></div>`
      );
    });
}


function execute(resId, relayId, duration) {
  fetch('/api/execute', {
    credentials: 'same-origin',
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({residence_id:resId, relay_id:relayId, duration})
  })
  .then(r => r.ok ? r.json() : r.text().then(t=>Promise.reject(t)))
  .then(_ => {
    alert('Acción enviada con éxito');
    loadRelays(resId);
  })
  .catch(err => {
    alert(`Error al ejecutar acción: ${err}`);
  });
}
