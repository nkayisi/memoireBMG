// const tps = document.querySelectorAll('.tp');
// const tds = document.querySelectorAll('.td');
// const interros = document.querySelectorAll('.interro');
// const examens = document.querySelectorAll('.examen');
// const matricules = document.querySelectorAll('.matricule');

// let course_name = document.querySelector('table').id;



// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// // document.querySelector('#readCote').addEventListener('submit', (e) => {


// // });
  

// const sendData = ()=>{

//   let cotes = [];

//   for (let index = 0; index < matricules.length; index++) {
//     const matricule = matricules[index].innerHTML;
//     const tp = tps[index].value;
//     const td = tds[index].value;
//     const interro = interros[index].value;
//     const examen = examens[index].value;

//     cotes.push({
//         Matricule: matricule,
//         TP: tp,
//         TD: td,
//         Interro: interro,
//         Examen: examen
//     });
    

//   }

//   $.ajax({
//     url: 'js/',
//     data : {
//       cotes: JSON.stringify(cotes),
//       course_name: course_name
//     },
//     success: function (data) {
//         window.location.reload();
//     }
// });

// }


// // activate bootstrap tabs
// var triggerTabList = [].slice.call(document.querySelectorAll('#myTab a'))
// triggerTabList.forEach(function (triggerEl) {
//   var tabTrigger = new bootstrap.Tab(triggerEl)

//   triggerEl.addEventListener('click', function (event) {
//     event.preventDefault()
//     tabTrigger.show()
//   })
// })

let cote_fields = document.querySelectorAll('.cote');
  
for (let index = 0; index < cote_fields.length; index++) {
  const field = cote_fields[index];

  
  field.addEventListener('change', (e) => {
    val = e.target.value;
    id = e.target.id;
    
    if (val != ''){

      $.ajax({
        url: '/cotes/ajax/',
        data: {
          'cote': val,
          'travail_id': id
        },
        success: function (data) {
          console.log(data);
        }
      });

      // let d = field.parentNode.querySelector('.total');
      // console.log(d);
      // console.log(field);
      // if (d != null){
      //   d.innerHTML = Number(d.value)+Number(val);
      //   console.log(Number(d.value)+Number(val));
      // }

    }
  });
}


const total_moyenne = () => {

  let cotes = document.getElementsByTagName('tr')
    
    for (let index = 0; index < cotes.length; index++) {
      const field = cotes[index];

      total = 0;
      sommePonderation = 0;
      moyenne = 0

      let inputs = field.querySelectorAll('input.cote')
      let ponderations = field.querySelectorAll('input.ponderation')
      for (let index = 0; index < inputs.length; index++) {
        const fld = inputs[index];
        total += Number(fld.value);

        const ponderation = ponderations[index]
        sommePonderation+= Number(ponderation.value)

      }

      moyenne = (total/sommePonderation) * 5
      console.log('Ponderation', sommePonderation)
      console.log('total', total)

      let d = field.querySelector('.total');
      if (d != null){
        d.innerHTML = total;
      }
      let avg = field.querySelector('.moyenne');
      if (avg != null){
        avg.innerHTML = moyenne;
      }

    }
}


total_moyenne();








