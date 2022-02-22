var sliders = document.getElementsByClassName("slider");
var values = document.getElementsByClassName("slider-value");
for (i = 0; i < sliders.length; i++) {
    // Display initial value for each slider
    values[i].innerHTML = sliders[i].value;
}

// On input change update displayed value for each slider
$('input.slider').on('input click change', function () {
   $(this).next().html($(this).val())
});