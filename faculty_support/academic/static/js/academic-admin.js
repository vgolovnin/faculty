(function($){
    function togglePhd(){
        const phd = $("#id_phd").parent();
        if ($("#id_degree").val() === "NO")
        {
            phd.hide();
            phd.parent().find(".errorlist").hide();
        }
        else
        {
            phd.show();
            const calendarnum = phd.find("a[id^=calendarlink]").attr("id").substr(12);
            DateTimeShortcuts.openCalendar(calendarnum);
        }
    }

    $(function(){
        $("#id_degree").change(function (e) {
            e.preventDefault();
            e.stopPropagation();
            setTimeout(togglePhd, 500);
        });
        togglePhd();
    });
})(django.jQuery);