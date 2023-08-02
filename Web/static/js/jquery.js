$(document).ready(function () {
  var graficaprediccion




  function recomendacion() {
    $.ajax({
      url: '/recomendacion',
      type: 'POST',
      success: function (data) {
        $('#titulo').html(data['titulo']);
        $('#miniatura').attr("src", data['miniatura']);
        $('#id').attr("href", "/receta/ver_video/" + data['id']);
      }
    });
  }
  $('#recomendacion-form').submit(function (event) {
    event.preventDefault();
    recomendacion();

  });
  // ---------- Fin Función recomendación ------------------ 
  // ---------- Gráfica todas las carnes ------------------
  statstotal()
  function statstotal() {
    $.ajax({
      url: '/stats',
      type: 'POST',
      success: function (data) {
        let vaca = data['cantidadvaca'];
        let pollo = data['cantidadpollo'];
        let cerdo = data['cantidadcerdo'];
        new Chart(document.getElementById("stats"), {
          type: 'bar',
          data: {
            labels: ["Carne de Vaca", "Carne de Pollo", "Carne de Cerdo"],
            datasets: [
              {
                label: "Kilogramos",
                backgroundColor: ["#ff6473", "#fbcf4b", "#7fbf4d"],
                data: [vaca, pollo, cerdo, 0]
              }
            ]
          },
          options: {
            legend: { display: false },
            title: {
              display: true,
              text: 'Carne que se compró a lo largo de la semana'
            },
            animation: {
              duration: 3000,
              easing: 'linear'
            },
          }
        });
      }
    });
  }


  // backgroundColor: ["#ff6473", "#4D90FE", "#7fbf4d"],
  // ---------- Fin Gráfica todas las carnes ------------------ 


  // ---------- Gráfica todas las carnes ------------------
  // consumo()
  // function consumo() {
  //   $.ajax({
  //     url: '/recomendacion',
  //     type: 'POST',
  //     success: function (data) {
  //       new Chart(document.getElementById("consumo"), {
  //         type: 'bar',
  //         data: {
  //           labels: ["Fecha 1", "Fecha 2", "Fecha 3", "Ayer"],
  //           datasets: [
  //             {
  //               label: "Restante",
  //               backgroundColor: ["#ff6473", "#fbcf4b", "#7fbf4d", "#4D90FE"],
  //               data: [0,3,5,1]
  //             }
  //           ]
  //         },
  //         options: {
  //           legend: { display: false },
  //           title: {
  //             display: true,
  //             text: 'Carbe restante de los días pasados'
  //           },
  //           animation: {
  //             duration: 3000,
  //             easing: 'linear'
  //           },
  //         }
  //       });
  //     }
  //   });
  // }
  // ---------- Fin Gráfica todas las carnes ------------------ 


  // ---------- Función stats lineal ------------------
  statslineal()
  function statslineal() {
    $.ajax({
      url: '/statslineal',
      type: 'POST',
      success: function (data) {
        new Chart(document.getElementById("statslineal"), {
          type: 'line',
          data: {
            labels: [data['carnecomprada'][0]['fecha'], data['carnecomprada'][1]['fecha'], data['carnecomprada'][2]['fecha'], data['carnecomprada'][3]['fecha'], data['carnecomprada'][4]['fecha'], data['carnecomprada'][5]['fecha'], data['carnecomprada'][6]['fecha']],
            datasets: [
              {
                data: [data['carnecomprada'][0]['cantidad'], data['carnecomprada'][1]['cantidad'], data['carnecomprada'][2]['cantidad'], data['carnecomprada'][3]['cantidad'], data['carnecomprada'][4]['cantidad'], data['carnecomprada'][5]['cantidad'], data['carnecomprada'][6]['cantidad']],
                label: "Carne Comprada",
                borderColor: "#4D90FE",
                pointBorderWidth: 5,
                fill: false
              },
              {
                data: [data['carneocupada'][0]['cantidad'], data['carneocupada'][1]['cantidad'], data['carneocupada'][2]['cantidad'], data['carneocupada'][3]['cantidad'], data['carneocupada'][4]['cantidad'], data['carneocupada'][5]['cantidad'], data['carneocupada'][6]['cantidad']],
                label: "Carne Ocupada",
                borderColor: "#fbcf4b",
                pointBorderWidth: 5,
                fill: true
              }, {
                data: [data['carneguardada'][0]['cantidad'], data['carneguardada'][1]['cantidad'], data['carneguardada'][2]['cantidad'], data['carneguardada'][3]['cantidad'], data['carneguardada'][4]['cantidad'], data['carneguardada'][5]['cantidad'], data['carneguardada'][6]['cantidad']],
                label: "Carne Guardada",
                borderColor: "#ff6473",
                fill: false,
                pointBorderWidth: 5
                // borderDash: [10, 10],
                // lineTension: 0
                // borderWidth: 10
                // pointBackgroundColor: "#fff600"
              },
            ]
          },
          options: {
            responsive: true,
            title: {
              display: true,
              text: 'Carne comprada y ocupada en los últimos 7 días'
            },
            animation: {
              duration: 2000,
              easing: 'linear'
            },
          }
        });
      }
    });
  }
  // ---------- Fin Función stats lineal ------------------ 

  // Nuevo Char
  prediccion()
  function prediccion() {
    $.ajax({
      url: '/prediccion',
      type: 'POST',
      success: function (data) {
        graficaprediccion = new Chart(document.getElementById("prediccion"), {
          type: 'line',
          data: {
            labels: [data['carne'][7]['fecha'], data['carne'][8]['fecha'], data['carne'][9]['fecha'], data['carne'][10]['fecha'], data['carne'][11]['fecha'], "Ayer", "Hoy"],
            datasets: [{
              data: [data['carne'][7]['cantidad'], data['carne'][8]['cantidad'], data['carne'][9]['cantidad'], data['carne'][10]['cantidad'], data['carne'][11]['cantidad'], data['carne'][12]['cantidad'], data['carne'][13]['cantidad']],
              label: "Kilogramos",
              borderColor: "#4D90FE",
              backgroundColor: "rgba(77, 145, 255, 0.5)",
              pointHoverRadius: 10,
              pointHitRadius: 10,
              pointBorderWidth: 15,
              fill: true,
              borderDash: [10, 10],
            },
            {
              data: [data['carne'][0]['cantidad'], data['carne'][1]['cantidad'], data['carne'][2]['cantidad'], data['carne'][3]['cantidad'], data['carne'][4]['cantidad'], data['carne'][5]['cantidad'], data['carne'][6]['cantidad']],
              label: "Semana Pasada",
              borderColor: "#ff6473",
              pointBorderWidth: 3,
              backgroundColor: "rgba(255, 102, 117, 0.03)",
              fill: true
            }
            ]
          },
          options: {
            responsive: true,
            title: {
              display: true,
              text: 'Carne ocupada en los últimos 7 días',
            },
            animation: {
              duration: 500,
              easing: 'linear'
            },
          }
        });
        // FIn nuevo Char
      }
    });
  }
  // ---------- Fin Regresión Lieal ------------------
  const botoncolor = document.querySelector('#switch');
  botoncolor.addEventListener('click', () => {
    $.ajax({
      success: function (data) {
        if (document.body.classList.contains('dark')) {
          graficaprediccion.label.fontColor = '#fff'

          graficaprediccion.update()
          // console.log(graficaprediccion)
          // graficaprediccion.update()

        } else {
          // graficaprediccion.defaults.defaultFontColor = '#777';
          // console.log("modo light")
          // graficaprediccion.update()
        }
      }
    })
  })

  // Predicciones para cada tipo de carne y corte
  predecir_cortes_y_tipo()
  function predecir_cortes_y_tipo() {
    var predicciongrafica = new Array();
    $.ajax({
      url: '/prediccion',
      type: 'POST',
      success: function (data) {
        predicciongrafica = data;
      }
    });
    $.ajax({
      url: '/predecircortesytipo',
      type: 'POST',
      success: function (data) {
        IA_llamado(data, predicciongrafica);
      }
    });

  }

  // Ejecutar la IA de forma secuencial
  async function IA_llamado(data, arreglografica) {
    var arreglocerdo = new Array();
    var arreglopollo = new Array();
    for (i = 0; i < data['carnes'].length; i++) {
      if (data['carnes'][i]['tipo'] == 2) {
        arreglocerdo.push(data['carnes'][i])
      } else {
        arreglopollo.push(data['carnes'][i])
      }
    }
    //Predicción de todas las carnes + Cargar en la gráfica la predicción
    let prediccionTotal = await InteligenciaArtificial(arreglografica['carne'])
    console.log(prediccionTotal);
    graficaprediccion.data.datasets[1].data[7] = arreglografica['carne'][7]['cantidad']; //Rojo
    graficaprediccion.data.labels[7] = "Mañana";
    graficaprediccion.data.datasets[0].data[7] = prediccionTotal.toFixed(1); //Azul
    graficaprediccion.update();
    document.getElementById("comprar").innerText = prediccionTotal.toFixed(1);
    // Predicción de cada tipo de carne Vaca, pollo, cerdo + creación de divs en home
    // let vaca = await InteligenciaArtificial(data['carnes']);
    let vaca = await InteligenciaArtificial(arreglografica['carne']);
    await crear_div_recomendado(vaca, "vaca");
    let pollo = await InteligenciaArtificial(arreglopollo);
    await crear_div_recomendado(pollo, "pollo");
    let cerdo = await InteligenciaArtificial(arreglocerdo);
    await crear_div_recomendado(cerdo, "cerdo");

  }

  // Función para crear div en el home con cada recomendación
  async function crear_div_recomendado(cantidad, tipo) {
    // kg = parseInt(cantidad) + " kg.";
    kg = cantidad.toFixed(1) + " kg.";
    imagen = "../static/img/" + tipo + ".png";
    var bloque = document.getElementById('contenedor_recomendado');
    var div_bloque_recomendado = document.createElement('div');
    div_bloque_recomendado.setAttribute('class', 'bloque_recomendado animate__animated animate__backInRight');
    bloque.appendChild(div_bloque_recomendado);

    var bloque_1 = document.createElement('div');
    bloque_1.setAttribute('class', 'bloque_recomendado_dentro bloque_1');
    var bloque_2 = document.createElement('div');
    bloque_2.setAttribute('class', 'bloque_recomendado_dentro bloque_2');
    div_bloque_recomendado.appendChild(bloque_1);
    div_bloque_recomendado.appendChild(bloque_2);

    var img = document.createElement('img');
    img.setAttribute('src', imagen);
    bloque_1.appendChild(img);

    var label = document.createElement('label');
    label.setAttribute('class', 'label_recomendacion');
    label.setAttribute('style', 'margin:0;');
    bloque_2.appendChild(label);
    $('.label_recomendacion').text('Recomendación');
    var p = document.createElement('p');
    p.setAttribute('class', 'p_recomendacion '+ tipo);
    bloque_2.appendChild(p);
    if(tipo == "vaca"){
      $('.vaca').text(kg);
    }else if(tipo == "pollo"){
      $('.pollo').text(kg);
    }else{
      $('.cerdo').text(kg);
    }
    
  }

  // let animado = document.querySelectorAll(".scrollanimado");
  // function mostrarScroll() {
  //   let scrollTop = document.documentElement.scrollTop;
  //   console.log(scrollTop)
  //   for (let i = 0; i < animado.length; i++) {
  //     let alturaAnimado = animado[i].offsetTop;
  //     if (scrollTop  >= 600) {
  //       animado[i].style.opacity = 1;

  //     }
  //   }
  // }
  // window.addEventListener('scroll', mostrarScroll);

  // ----------------- Inteligencia Artificial -----------------
  async function InteligenciaArtificial(arreglo) {
    var valX = []
    var valY = []
    if (arreglo.length > 15) {
      longitud = 15;
    } else if (arreglo.length <= 15) {
      longitud = arreglo.length;
    }
    for (i = 0; i < longitud; i++) {
      valX.push(i+1)
      valY.push(arreglo[i]['cantidad'])
    }
    //Definimos el modelo que sera de regresion lineal
    const model = tf.sequential();
    //Agregamos una capa densa porque todos los nodos estan conectado entre si
    model.add(tf.layers.dense({ units: 1, inputShape: [1] }));

    // Compilamos el modelo con un sistema de perdida de cuadratico y optimizamos con sdg
    model.compile({ loss: 'meanSquaredError', optimizer: 'sgd' });
    // Creamos los tensores para x y para y
    const xs = tf.tensor2d(valX, [valX.length, 1]);
    const ys = tf.tensor2d(valY, [valY.length, 1]);
    // Obtenemos la epocas (Las veces que se repetira para encontrar el valor de x)
    var epocas = 500;
    // Obtenemos el valor de x
    var nuevoValX = valX.length;
    // Ciclo que va ir ajustando el calculo
    for (i = 0; i < epocas; i++) {
      // Entrenamos el modelo una sola vez (pero como esta dentro de un ciclo se va ir entrenando por cada bucle)
      await model.fit(xs, ys, { epochs: 1 });
      // Obtenemos el valor de Y cuando el valor de x sea
      var prediccionY = model.predict(tf.tensor2d([nuevoValX], [1, 1])).dataSync()[0];
    }
    console.log(prediccionY);
    return prediccionY;
  }

  //Fin

})
