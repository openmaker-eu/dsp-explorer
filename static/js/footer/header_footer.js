/**
 * Created by andreafspeziale on 17/05/17.
 */
(function($){

    function re_render () {
        var header_padding = 30;
        var header_margin = 20;
        var header_border = 1;
        var content_height = $('#top-div').height();
        var footer_height = $('#footer').height();
        var body_height = $('body').height();

        if ((content_height + footer_height) < body_height) {
            $('#top-div').height(body_height - footer_height)
        }

        $("body").css("padding-top", $(".navbar").height() + header_padding + header_margin + header_border);
        console.log($(".navbar").height());
    }

    $(window).on('resize', re_render);

    $( document ).ready( function(){
        re_render();
    })
})(jQuery);