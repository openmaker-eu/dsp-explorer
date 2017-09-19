/**
 * Created by andreafspeziale on 17/05/17.
 */
(function($){

    function re_render () {

        var header_padding = 30;
        var header_margin = 20;
        var header_border = 1;

        var height_needed = $(".navbar").height() + header_padding + header_margin + header_border

        var spacer = $("#spacer").length === 0 ? $('<div id="spacer"></div>').prependTo("body") : $("#spacer")

        spacer.css("height", height_needed)

        var body_height = $('body').height();
        var content_height = $('#top-div').height();
        var footer_height = $('#footer').height();

        if((height_needed + content_height + footer_height) < body_height) {
            console.log("push dat shit")
            $('#top-div').height(body_height - height_needed - footer_height)
        }

    }

    $(window).on('resize', re_render);

    $( document ).ready( function(){
        re_render();
    })
})(jQuery);