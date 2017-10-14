$(document).ready(function () {

    // Get the modal_container
    var modal_container = document.getElementById('id_modal_container');
    var modal_img = document.getElementById("id_modal_img");
    var modal_caption = document.getElementById("id_modal_caption");

    $(".item_img_thumb").click(function () {
        modal_container.style.display = "block";
        modal_img.src = this.src;
        modal_caption.innerHTML = this.alt;
    });

    // Get the <modal_span> element that closes the modal_container
    var modal_span = document.getElementsByClassName("modal_close")[0];

    // When the user clicks on <modal_span> (x), close the modal_container
    modal_span.onclick = function () {
        modal_container.style.display = "none";
    };

    alert('ready');
});
