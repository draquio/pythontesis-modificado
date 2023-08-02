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

// function agregar_campo_corte() {
//   // $.ajax({
//   //   url: '/agregarcampocorte',
//   //   type: 'POST',
//   //   success: function (data) {
//       var selector_tipo_carne = document.querySelector('tipo-corte-carne');
//       console.log(selector_tipo_carne)
//       var bloque_cortes = document.getElementById('bloque_cortes');
//       var nuevoCampoKg = document.createElement('input');
//       nuevoCampoKg.setAttribute('type', 'number');
//       nuevoCampoKg.setAttribute('name', 'corte[]');
//       nuevoCampoKg.setAttribute('class', 'form-control cantidad-corte-carne');
//       nuevoCampoKg.setAttribute('placeholder', 'Kg.');


//       var nuevoCampoTipo = document.createElement('select');
//       nuevoCampoTipo.setAttribute('class', 'form-control tipo-corte-carne');
//       nuevoCampoTipo.setAttribute('name', 'corte-carne');

//       bloque_cortes.appendChild(nuevoCampoKg);
//       bloque_cortes.appendChild(nuevoCampoTipo);
//     // }
//   // });
// }

    // //Multiples inserciones
    // function CargarCarneArreglo() {
    //   var arregloCarnes = new Array();
    //   var valoresInputs = document.getElementsByClassName('cantidad-corte-carne');
    //   nombreValores = [].map.call(valoresInputs,function(data){
    //     arregloCarnes.push(data.value);
    //   })
    //   console.log(arregloCarnes)
    // }







  // agregar_campo_corte.onclick = function(){
  //   alert("pruebaa")
  //   var nuevoCampo = document.createElement('input');
  //   nuevoCampo.setAttribute('type', 'number');
  //   nuevoCampo.setAttribute('name','corte');
  //   nuevoCampo.setAttribute('class', 'form-control cantidad-corte-carne');
  //   bloque_cortes.appendChild(nuevoCampo);
  // }