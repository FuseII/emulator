const downloadReportButton = document.getElementById("download-report-button")
downloadReportButton.addEventListener('click', downloadReport);


async function downloadReport(event) {
console.log("clicked");
    try {
        window.open('/pages/file/download');
        const response = await fetch('/pages/file/download');
        console.log(response);

        // Проверяем успешность ответа
        // if (!response.ok) {
        //     // Получаем данные об ошибке
        //     const errorData = await response.json();
        //     // console.log(errorData);  // Отображаем ошибки alert
        //     alert(errorData.detail);
        // }
    } catch (error) {
        // console.error('Error:', error)
        alert('Ошибка:  ' + error);
    }

}