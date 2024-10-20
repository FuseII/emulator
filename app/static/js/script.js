// const clickButton = document.querySelector('button');
// clickButton.addEventListener('click', calculate);
// clickButton.addEventListener('click', calculate);
const enterDataButton = document.getElementById("enter-data-button")
enterDataButton.addEventListener('click', enterData);
const savedBackgroundBtn = enterDataButton.style.background;
const disabledBackgroundBtn = 'grey';


const nextStepButton = document.getElementById("next-step-button")
nextStepButton.addEventListener('click', next_step);
nextStepButton.disabled = true
nextStepButton.style.background = disabledBackgroundBtn;

const resetButton = document.getElementById("reset-button")
resetButton.addEventListener('click', reset);
resetButton.disabled = true
resetButton.style.background = disabledBackgroundBtn;

const runAllButton = document.getElementById("run-all-button")
runAllButton.addEventListener('click', run_all);
runAllButton.disabled = true
runAllButton.style.background = disabledBackgroundBtn;


async function updateSliderValue(value) {
    console.log(value)
    // console.log(clickButton.id)
    let slider = document.getElementById('slider');
    let output = document.getElementById('sliderValue');
    output.innerHTML = slider.value;
    let array_1 = document.getElementById('array_1');
    let array_2 = document.getElementById('array_2');
    let ths = ""
    let trs = ""
    for (let i = 0; i < slider.value; i++) {
        ths += "<th>" + "Элемент " + i + "</th>";
        // let element_id = 'element_' + i.toString();
        trs += "<td><input type='number' min='0' step='1'  value='0'></td>";
        // trs += "<td><input type='number' min='0' step='1'  value='0' id=" + element_id + "></td>";
        // trs += "<td>" + i + "</td>";
    }
    let talble = "<table><thead><tr>" + ths + "</thead><tbody><tr>" + trs + "</tbody></table>";
    array_1.innerHTML = talble;
    // array_2.innerHTML = talble;
    if (array_2 != null) {
        array_2.innerHTML = talble;
    }
    tableId = 'table-flags';
    data = {'PC': 1, 'SF': 0, 'ZF': 6, 'CF': 5};
    displayDataInTable(tableId, data);
}

function displayDataInTable(tableId, data) {

    let headers = Object.keys(data);

    //Prepare html header
    var headerRowHTML = '<tr>';
    var allRecordsHTML = '';
    allRecordsHTML += '<tr>';
    for (var i=0;i<headers.length;i++) {
        headerRowHTML += '<th>' + headers[i]+ '</th>';
        console.log(headers);
        allRecordsHTML += '<td>' + data[headers[i]] + '</td>';

    }
    headerRowHTML += '</tr>';
    headerRowHTML = '<thead>' + headerRowHTML + '</thead>'
    allRecordsHTML += '</tr>';
    allRecordsHTML = '<tbody>' + allRecordsHTML + '</tbody>'

    //Append the table header and all records
    let table = document.getElementById(tableId);
    table.innerHTML = headerRowHTML + allRecordsHTML;

}

// window.addEventListener("load", updateSliderValue);

async function enterData(event) {
    console.log("btn");
    const data = []

    let table = document.getElementById("array_1");
    let data_output = document.getElementById("enter-data-output");
    for (var i = 1, row; row = table.rows[i]; i++) {
        for (var j = 0, col; col = row.cells[j]; j++) {
            const input = col.querySelector('input');
            data.push(parseInt(input.value, 10)); // Получаем значение из input и преобразуем в число
        }
    }
    console.log(data); // Вывод двумерного массива с данными из таблицы


    let code_text = document.getElementById("code_text");
    console.log(code_text.value);
    let text = code_text.value
    let send_data = {"array": data, "text": text};
    //GET запрос?
    try {
        const response = await fetch('/pages/enter_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(send_data)
        });

        // Проверяем успешность ответа
        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            console.log(errorData);  // Отображаем ошибки alert
            return;  // Прерываем выполнение функции
        }

        const result = await response.json();

        if (result.message) {
            console.log(result.message);
            data_output.value = result.message;
            resetButton.style.background = savedBackgroundBtn;
            resetButton.disabled = false;
            nextStepButton.style.background = savedBackgroundBtn;
            nextStepButton.disabled = false;
            runAllButton.style.background = savedBackgroundBtn;
            runAllButton.disabled = false;
        } else {
            alert('Неизвестная ошибка');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка ');
    }

}


async function next_step(event) {

    let code_text = document.getElementById("code_text");
    console.log("next step");
    let text = code_text.value
    let send_data = {"text": text}
    let program_output_info = document.getElementById("program_output_info");

    try {
        const response = await fetch('/pages/next_step');

        // Проверяем успешность ответа
        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            console.log(errorData);  // Отображаем ошибки alert
            alert('Error ' + errorData.detail);
            return;  // Прерываем выполнение функции
        }
        const result = await response.json();

        if (result.message) {
            console.log(result);
            program_output_info.value = result.message;
            runAllButton.style.background = disabledBackgroundBtn;
            runAllButton.disabled = true;
            if (result['program_finished']) {
                nextStepButton.style.background = disabledBackgroundBtn;
                nextStepButton.disabled = true;
            }
        } else {
            alert('Неизвестная ошибка');
        }
    } catch (error) {
        // console.error('Error:', error)
        alert('Ошибка:  ' + error);
    }

}

async function reset(event) {

    try {
        const response = await fetch('/pages/reset');

        // Проверяем успешность ответа
        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            console.log(errorData);  // Отображаем ошибки alert
            alert('Error ' + errorData.detail);
            return;  // Прерываем выполнение функции
        }
        const result = await response.json();

        if (result.message) {
            console.log(result.message);
            program_output_info.value = result.message;
            resetButton.style.background = savedBackgroundBtn;
            resetButton.disabled = false;
            nextStepButton.style.background = savedBackgroundBtn;
            nextStepButton.disabled = false;
            runAllButton.style.background = savedBackgroundBtn;
            runAllButton.disabled = false;
        } else {
            alert('Неизвестная ошибка');
        }
    } catch (error) {
        // console.error('Error:', error)
        alert('Ошибка:  ' + error);
    }

}

async function run_all(event) {

    try {
        const response = await fetch('/pages/run_all');

        // Проверяем успешность ответа
        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            console.log(errorData);  // Отображаем ошибки alert
            alert('Error ' + errorData.detail);
            return;  // Прерываем выполнение функции
        }
        const result = await response.json();

        if (result.message) {
            console.log(result.message);
            program_output_info.value = result.message;
            nextStepButton.style.background = disabledBackgroundBtn;
            nextStepButton.disabled = true;

        } else {
            alert('Неизвестная ошибка');
        }
    } catch (error) {
        // console.error('Error:', error)
        alert('Ошибка:  ' + error);
    }

}