$(document).ready(function () {

    $(".masonry-img-thumb").click(function () {
        $('#id_modal_container').css('display', 'block');
        // $('#id_modal_img').attr('src', this.src);
        $('#id_modal_details').html(this.parentElement.innerHTML);
    });

    // Get the <modal_span> element that closes the modal_container
    var modal_span = document.getElementsByClassName("modal_close")[0];

    // When the user clicks on <modal_span> (x), close the modal_container
    modal_span.onclick = function () {
        $('#id_modal_container').css('display', 'none');
    };
});
