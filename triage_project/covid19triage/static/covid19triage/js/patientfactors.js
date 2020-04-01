document.addEventListener("readystatechange", event => {
    if (event.target.readyState === "complete") {
        var feverCheckbox = document.querySelector("input[type='checkbox'][value='fever']");

        feverCheckbox.addEventListener("change", () => {
            ShowTemperatureFormRow(feverCheckbox);
        });

        // Handle page reload
        ShowTemperatureFormRow(feverCheckbox);
    }
});

function ShowTemperatureFormRow(checkboxInput) {
    var temperatureFormRow = document.querySelector("div.form-row.temperature");
    var temperatureInput = document.getElementById("id_temperature");

    if (checkboxInput.checked) {
        temperatureFormRow.style.display = "block";
    } else {
        temperatureFormRow.style.display = "none";
        temperatureInput.value = "";
    }
}
