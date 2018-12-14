/**
 * Created by SPREADTRUM\pl.dong on 18-12-13.
 */
$(function () {
    function setfooter() {

        var bodyY = $(document.body).height();
        var documentY = $(document).height();
        $('.footer').css('top',(documentY-100)+'px')
    }
    setfooter();
});