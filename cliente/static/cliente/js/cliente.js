$(document).ready(function() {
   // Stuff to do as soon as the DOM is ready
   info_cliente();
});


function info_cliente(){
  $("body").append('<div id="contenedor"></div>');
  $(".cliente").click(function(event) {
    /* Act on the event */
    var id = $(this).attr("id");
    $("#contenedor").load("/info/cliente/"+id+"/",function() {
      /* Act on the event */
      $("#cliente_single").modal('show');
      $("#suit_form_tabs").suit_form_tabs();
    });
  });
}
