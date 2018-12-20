/**
 * Created by SPREADTRUM\pl.dong on 18-12-15.
 */
$(function () {
    //让footer不会因为log的显示导致不能始终在最底下
    $('.footer').css('position', 'static');

    $('#lava_job_info_log, #lava_job_info_yaml').on('click', function () {
        $(this).next().children().slideToggle('1s');
        // $(this).next().children().toggleClass('display_none');
    });

    $(".f-button").on('click', function () {
        $('html, body').animate({scrollTop: 0});
    });

    $(window).scroll(function () {
        if ($(this).scrollTop()<900){
            $('.f-button').fadeOut();
        }else {
            $('.f-button').fadeIn();
        }
    });
});