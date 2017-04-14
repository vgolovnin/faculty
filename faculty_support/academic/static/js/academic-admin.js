(function($){
    function togglePhd(calendar=true){
        const phd = $("#id_phd");
        if ($("#id_degree").val() == "")
        {
            phd.val('');
            phd.parent().hide();
            phd.parent().parent().find(".errorlist").hide();
        }
        else
        {
            phd.parent().show();
            if (calendar) {
                const calendarnum = phd.parent().find("a[id^=calendarlink]").attr("id").substr(12);
                DateTimeShortcuts.openCalendar(calendarnum);
            }
        }
    }

    $(function(){
        $("#id_degree").change(function (e) {
            e.preventDefault();
            e.stopPropagation();
            setTimeout(togglePhd, 500);
        });
        togglePhd(false);
    });
})(django.jQuery);