(function($){
    function togglePhd(){
        const phd = $("#id_phd").parent();
        try {
            if ($("#id_degree").val() === "Нет")
            {
                phd.hide();
                phd.parent().find(".errorlist").hide();
            }
            else
            {
                phd.show();
                const calendarnum = phd.find(".date-icon").parent().attr("id").substr(12);
                DateTimeShortcuts.openCalendar(calendarnum);
            }
        } catch (err) {}
    }
    $(function(){
        $("#id_degree").change(togglePhd);
        togglePhd();
    });
})(django.jQuery);