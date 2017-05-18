/**
 * Created by andreafspeziale on 17/05/17.
 */
(function($){

    function re_render () {
        var content_height = $('#top-div').height();
        var footer_height = $('#footer').height();
        var body_height = $('body').height();

        if ((content_height + footer_height) < body_height) {
            $('#top-div').height(body_height - footer_height)
        }
    }

    $(window).on('resize', re_render);

    $( document ).ready( function(){
        re_render();
    })
})(jQuery);