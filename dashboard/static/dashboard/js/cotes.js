const tps = document.querySelectorAll('.tp');
const tds = document.querySelectorAll('.td');
const interros = document.querySelectorAll('.interro');
const examens = document.querySelectorAll('.examen');
const matricules = document.querySelectorAll('.matricule');

let course_name = document.querySelector('table').id;



const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// document.querySelector('#readCote').addEventListener('submit', (e) => {


// });
  

const sendData = ()=>{

  let cotes = [];

  for (let index = 0; index < matricules.length; index++) {
    const matricule = matricules[index].innerHTML;
    const tp = tps[index].value;
    const td = tds[index].value;
    const interro = interros[index].value;
    const examen = examens[index].value;

    cotes.push({
        Matricule: matricule,
        TP: tp,
        TD: td,
        Interro: interro,
        Examen: examen
    });
    

  }

  $.ajax({
    url: 'js/',
    data : {
      cotes: JSON.stringify(cotes),
      course_name: course_name
    },
    success: function (data) {
        window.location.reload();
    }
});

}










