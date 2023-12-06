$(function() {
  $('a[href*=#]').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({ scrollTop: $($(this).attr('href')).offset().top}, 500, 'linear');
  });
});

function validateForm() {
    var departureInput = document.getElementById('inputField1');
    var arrivalInput = document.getElementById('inputField2');
    var empty = false;

    if (departureInput.value.trim() === '') {
        empty = true;
        departureInput.style.border = '2px solid red';
    } else {
        departureInput.style.border = ''; // Reset border
    }

    if (arrivalInput.value.trim() === '') {
        empty = true;
        arrivalInput.style.border = '2px solid red';
    } else {
        arrivalInput.style.border = ''; // Reset border
    }
        // Add any additional validation
    return !empty;
}
function popupP() {
  var popup = document.getElementById("error");
  popup.classList.toggle("show");
}
function showPopup() {
    var popup = document.getElementById("myPopup");
    popup.style.display = "block";
    setTimeout(function () {
        popup.style.display = "none";
    }, 3000);  // Hide the popup after 3 seconds (adjust as needed)
}
