
function agregarcampocorte() {
    $.ajax({
        url: '/agregarcampocorte',
        type: 'POST',
        success: function (data) {
            var bloque_carne_izquierda = document.getElementById('bloque_carne_izquierda');
            var bloque_carne_derecha = document.getElementById('bloque_carne_derecha');
            var nuevoCampoKg = document.createElement('input');
            nuevoCampoKg.setAttribute('type', 'number');
            nuevoCampoKg.setAttribute('name', 'corte[]');
            nuevoCampoKg.setAttribute('class', 'form-control cantidad-corte-carne');
            nuevoCampoKg.setAttribute('placeholder', 'Cantidad en kg.');


            var nuevoCampoTipo = document.createElement('select');
            nuevoCampoTipo.setAttribute('class', 'form-control tipo-corte-carne');
            nuevoCampoTipo.setAttribute('name', 'corte-carne[]');

            bloque_carne_izquierda.appendChild(nuevoCampoKg);
            bloque_carne_derecha.appendChild(nuevoCampoTipo);
            for (var i=0; i < data.length; i++){
                nuevoCampoTipo.options[i] = new Option(data[i].nombre,data[i].id);
            }
        }
    });
}
function seleccionarTipoCarne(){
    let tipocarne = document.getElementById('tipocarne');
    let valor = tipocarne.value;
    if(valor == 1){
        document.getElementById('bloque_cantidad').style.display = 'none';
        $("#bloque_cortes").show();
    }else{
        $("#bloque_cortes").hide();
        document.getElementById('bloque_cantidad').style.display = 'block';
    }
}
//Elimina espacios en Agregar_carne
function eliminar_campos_corte(){
    let bloque_carne_derecha = document.getElementById('bloque_carne_derecha');
    let bloque_carne_izquierda = document.getElementById('bloque_carne_izquierda');
    var select_tag = bloque_carne_derecha.getElementsByTagName('select');
    var input_tag = bloque_carne_izquierda.getElementsByTagName('input');
    if(select_tag.length > 1){
        bloque_carne_derecha.removeChild(select_tag[(select_tag.length) - 1]);
    }
    if(input_tag.length > 1){
        bloque_carne_izquierda.removeChild(input_tag[(input_tag.length) - 1]);
    }
}

//Elimina espacios en Guardar_Carne
function eliminar_campos_carne(){
    let bloque_izquierda = document.getElementById('guardar_bloque_carne_izquierda');
    let bloque_centro = document.getElementById('guardar_bloque_carne_centro');
    let bloque_derecha = document.getElementById('guardar_bloque_carne_derecho');

    var input_tag = bloque_izquierda.getElementsByTagName('input');
    var select_tag = bloque_centro.getElementsByTagName('select');
    var select_tag_almacen = bloque_derecha.getElementsByTagName('select');

    if(select_tag.length > 1){
        bloque_izquierda.removeChild(input_tag[(input_tag.length) - 1]);
        bloque_centro.removeChild(select_tag[(select_tag.length) - 1]);
        bloque_derecha.removeChild(select_tag_almacen[(select_tag_almacen.length) - 1]);
    }
}

// Multiples inserciones
// function CargarCarneArreglo() {
//     var arregloCarnes = new Array();
//     var arregloTipo = new Array();
//     var valoresInputs = document.getElementsByClassName('cantidad-corte-carne');
//     var valoresTipos = document.getElementsByClassName('tipo-corte-carne');
//     nombreValores = [].map.call(valoresInputs,function(data){
//       arregloCarnes.push(data.value);
//     });
//     valorTipo = [].map.call(valoresTipos,function(data){
//         arregloTipo.push(data.value);
//     });
//     console.log(arregloTipo);
//   }



// ------------- Funciones Guardar Carne ----------------
function agregarcampoguardarcarne() {
    $.ajax({
        url: '/agregarcampocorte',
        type: 'POST',
        success: function (data) {
            var guardar_bloque_carne_derecho = document.getElementById('guardar_bloque_carne_derecho');

            var nuevoCampoKg = document.createElement('input');
            nuevoCampoKg.setAttribute('type', 'number');
            nuevoCampoKg.setAttribute('min', '1');
            nuevoCampoKg.setAttribute('name', 'corte[]');
            nuevoCampoKg.setAttribute('class', 'form-control cantidad-corte-carne');
            nuevoCampoKg.setAttribute('placeholder', 'Cantidad en kg.');


            var nuevoCampoTipo = document.createElement('select');
            nuevoCampoTipo.setAttribute('class', 'form-control tipo-corte-carne');
            nuevoCampoTipo.setAttribute('name', 'corte-carne[]');

            guardar_bloque_carne_izquierda.appendChild(nuevoCampoKg);
            guardar_bloque_carne_centro.appendChild(nuevoCampoTipo);
            for (var i=0; i < data.length; i++){
                nuevoCampoTipo.options[i] = new Option(data[i].nombre,data[i].id);
            }
            listaralmacenes();
        }
    });
}

function listaralmacenes() {
    $.ajax({
        url: '/listaralmacenes',
        type: 'POST',
        success: function (data) {
            console.log(data);
            var guardar_bloque_carne_derecho = document.getElementById('guardar_bloque_carne_derecho');
            var nuevoCampoAlmacen = document.createElement('select');
            nuevoCampoAlmacen.setAttribute('class', 'form-control tipo-corte-carne');
            nuevoCampoAlmacen.setAttribute('name', 'lista-almacen[]');

            guardar_bloque_carne_derecho.appendChild(nuevoCampoAlmacen);
            for (var i=0; i < data.length; i++){
                nuevoCampoAlmacen.options[i] = new Option(data[i].nombre,data[i].id);
            }
        }
    });
}