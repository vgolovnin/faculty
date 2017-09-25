<template>
<div class="reports">
<h4 class="reports-header">Отчёты</h4>
    <div v-for="(stages, name) in reports">
        <h5>{{ name }}</h5>
    <ul>
        <li v-for="stage in stages">
            {{ stage.stagename }}
             <a v-for="report in stage.templates" :href="stage.url +'/template/' + report.id" class="fi-page-export-doc"> {{ report.name }}</a>
        </li>
    </ul>
    </div>
</div>
</template>
<script>
import _ from 'lodash'
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
            return _.groupBy(this.report_stages, 'name')
        }
    },
}
</script>

<style scoped>
    .reports {
        margin: 10px 0 0 10px;
    }
    .reports ul > li
    {
        list-style: none;
    }
</style>