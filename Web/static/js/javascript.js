const btnSwitch = document.querySelector('#switch');

btnSwitch.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  document.body.classList.toggle('light');
  btnSwitch.classList.toggle('active');


  if (document.body.classList.contains('dark')) {
    localStorage.setItem('dark-mode', 'true');

  } else {
    localStorage.setItem('dark-mode', 'false');
  }

});
if (localStorage.getItem('dark-mode') === 'true') {
  document.body.classList.add('dark');
  document.body.classList.remove('light');
  btnSwitch.classList.add('active');
} else {
  document.body.classList.add('light');
  document.body.classList.remove('dark');
  btnSwitch.classList.remove('active');
}

// Mover lista
var URLactual = window.location.pathname;
if (URLactual == "/rol") {
  const lista = document.getElementById('lista');
  Sortable.create(lista, {
    animation: 150,
    chosenClass: "lista_selecionada",
    dragClass: "drag",
  });
}
