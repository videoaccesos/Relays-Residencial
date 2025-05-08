d// main.js - Panel Operador
document.addEventListener('DOMContentLoaded', () => {
  const resSelect = document.getElementById('res-select');
  const btnLoad = document.getElementById('btn-load');
  const grid = document.getElementById('relays-grid');

  fetch('/api/residences?page=1')
    .then(r => r.json())
    .then(list => list.forEach(r => {
      const o = document.createElement('option'); o.value = r.id; o.text = r.name;
      resSelect.add(o);
    }));

  btnLoad.addEventListener('click', () => {
    grid.innerHTML = '';
    fetch(`/api/residences/${resSelect.value}/relays`)
      .then(r => r.json())
      .then(relays => {
        while (relays.length < 16) relays.push({ relay_id: null, name: '', state: 'Off' });
        relays.slice(0,16).forEach(r => {
          const col = document.createElement('div'); col.className = 'p-2';
          const btn = document.createElement('button');
          btn.className = `btn btn-lg ${r.state==='On'? 'btn-danger' : 'btn-success'}`;
          btn.textContent = r.name || `R${r.relay_id}`;
          if (r.relay_id) btn.onclick = () => fetch('/api/execute', {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({ user:'op1',residence_id:resSelect.value,relay_id:r.relay_id,duration:2 })
          }).then(() => btnLoad.click());
          else btn.disabled=true;
          const input = document.createElement('input');
          input.type='text'; input.maxLength=10; input.value=r.name;
          input.className='form-control form-control-sm mt-1';
          input.disabled = !r.relay_id;
          input.onblur = () => fetch(`/api/residences/${resSelect.value}/relays/${r.relay_id}/name`, {
            method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ name: input.value })
          });
          col.append(btn,input);
          grid.appendChild(col);
        });
      });
  });
});