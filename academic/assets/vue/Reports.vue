<template>
                    <div class="reports">
<h4 class="reports-header">Отчёты</h4>
    <ul v-for="report_stage in reports">
        <li v-for="report in report_stage">
             <a :href="report.url" class="fi-page-export-doc"> {{ report.stagename }} [{{ report.name }}]</a></a>
        </li>
    </ul>
</div>

</template>
<script>
export default
{
    name: 'Reports',
    data: () => ({
        report_stages: []
    }),
    mounted: function () {
        this.$http.get(process.env.APP_URL + 'api/reports/').then(function (resp) {
                this.report_stages = resp.data;
            },
            function (resp) {
                console.log(resp);
            });

    },
    computed: {
        reports(){
            return _.mapValues(this.report_stages,
                report_stage => (
                    _.mapValues(report_stage.templates,
                        template => ({
                                name: template.name,
                                stagename: report_stage.stagename,
                                url: report_stage.url + "/template/" + template.id
                            }
                        ))
                )
            );
        }
    },
}
</script>

<style>
    .reports ul > li
    {
        list-style: none;
    }
</style>