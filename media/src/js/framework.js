/**
 * JavaScript Framework
 * @author Guillaume VanderEst <gui@exo.me>
 * @version 1.0.3
 */

/** Select boxes **/
$('select').each(function(){
    $(this).wrap('<span class="select"></span>');
});

/** Scalable objects **/
var $scale = function(){
    $('*[data-scale]').each(function(){
        $(this).removeAttr('width');
        $(this).removeAttr('height');
        $(this).width('100%');

        var $this = $(this);

        var width = $this.width();
        var scale = Number($this.attr('data-scale'));
        var height = width * scale;

        $this.height(height);
    });
    $('*[data-height]').each(function(){
        $(this).css('height', $(this).attr('data-height'));
    });
    $('*[data-width]').each(function(){
        $(this).css('width', $(this).attr('data-width'));
    });
    $('*[data-max-height]').each(function(){
        $(this).css('maxHeight', $(this).attr('data-max-height'));
    });
    $('*[data-max-width]').each(function(){
        $(this).css('maxWidth', $(this).attr('data-max-width'));
    });
};
$(window).ready(function(){
    $(window).on('resize', function(){
        $scale();
    });
    setTimeout(function(){
        $scale();
    }, 50);
});
