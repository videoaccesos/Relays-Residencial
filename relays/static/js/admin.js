// static/js/admin.js

document.addEventListener('DOMContentLoaded', () => {
  const btnNew = document.getElementById('btn-new-res');
  if (btnNew) {
    btnNew.addEventListener('click', () => {
      const id   = prompt('ID de la nueva residencia:');
      const name = prompt('Nombre:');
      const type = prompt('Tipo (html/xml):');
      const url  = prompt('URL base:');
      if (id&&name&&type&&url) {
        alert(`Crear residencia:\n${id} / ${name} / ${type} / ${url}`);
      }
    });
  }
});

function editResidence(id) {
  alert(`Editar residencia "${id}"`);
}
function deleteResidence(id) {
  if (confirm(`¿Borrar residencia "${id}"?`)) {
    alert(`Residencia "${id}" eliminada`);
  }
}
