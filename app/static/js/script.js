// const clickButton = document.querySelector('button');
// clickButton.addEventListener('click', calculate);
// clickButton.addEventListener('click', calculate);
const enterDataButton = document.getElementById("enter-data-button")
enterDataButton.addEventListener('click', enterData);

const calculateButton = document.getElementById("calculate-button")
calculateButton.addEventListener('click', next_step);


async function updateSliderValue(value) {
    console.log(value)
    // console.log(clickButton.id)
    let slider = document.getElementById('slider');
    let output = document.getElementById('sliderValue');
    output.innerHTML = slider.value;
    let array_1 = document.getElementById('array_1');
    let ths = ""
    let trs = ""
    for (let i = 0; i < slider.value; i++) {
        ths += "<th>" + "Элемент " + i + "</th>";
        let element_id = 'element_' + i.toString();
        trs += "<td><input type='number' min='0' step='1'  value='0' id=" + element_id + "></td>";
        // trs += "<td>" + i + "</td>";
    }
    let talble = "<table><thead><tr>" + ths + "</thead><tbody><tr>" + trs + "</tbody></table>";
    array_1.innerHTML = talble;

// event.preventDefault();  // Предотвращаем стандартное действие формы

    // Получаем форму и собираем данные из неё
    // const form = document.getElementById('registration-form');
    // const formData = new FormData(form);
    // const data = Object.fromEntries(formData.entries());
    //
    // try {
    //     const response = await fetch('/auth/register', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify(data)
    //     });
    //
    //     // Проверяем успешность ответа
    //     if (!response.ok) {
    //         // Получаем данные об ошибке
    //         const errorData = await response.json();
    //         displayErrors(errorData);  // Отображаем ошибки
    //         return;  // Прерываем выполнение функции
    //     }
    //
    //     const result = await response.json();
    //
    //     if (result.message) {  // Проверяем наличие сообщения о успешной регистрации
    //         window.location.href = '/pages/login';  // Перенаправляем пользователя на страницу логина
    //     } else {
    //         alert(result.message || 'Неизвестная ошибка');
    //     }
    // } catch (error) {
    //     console.error('Ошибка:', error);
    //     alert('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
    // }
}

// window.addEventListener("load", updateSliderValue);

async function enterData(event) {
    console.log("btn");
    const data = []

    var table = document.getElementById("array_1");
    var data_output = document.getElementById("enter-data-output");
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
    let send_data = {"array":data,"text":text};
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
    console.log(code_text.value);
    let text = code_text.value
    let send_data = {"text":text}
    let program_output_info = document.getElementById("program_output_info");

     try {
        const response = await fetch('/pages/next_step', {
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
            program_output_info.value = result.message;
        } else {
            alert('Неизвестная ошибка');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка ');
    }

}