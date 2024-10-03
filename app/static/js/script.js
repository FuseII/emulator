async function updateSliderValue(value) {
    console.log(value)
    let slider = document.getElementById('slider');
    let output = document.getElementById('sliderValue');
    output.innerHTML = slider.value;
    let array_1 = document.getElementById('array_1');
    let ths = ""
    let trs = ""
    for (let i = 0; i < slider.value; i++) {
        ths += "<th>" + "Элемент " + i + "</th>";
        trs += "<td><input type='number' min='0' step='1' id={'element'+i}/></td>";
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