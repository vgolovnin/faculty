<template>
    <div>
        <div v-for="(categories,status) in groupedReserve">
            <h4 class="status-header">Статус участия: {{ status }}</h4>
            <div v-for="(table, category) in categories">
                <h5>{{ category }}</h5>
                <table>
                    <thead>
                    <th style="width:300px;">Сотрудник</th>
                    <th style="width:200px;">Должность</th>
                    <th></th>
                    </thead>
                    <tr is="reservist-row" v-for="r in table" :res="r"
                        :part="filterParticipations(r)" :warnings="r.warnings" :key="r.url"></tr>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    import ReservistRow from './ReservistRow.vue'
    export default
    {
        name: "ReserveTable",
        data: () => ({
            reserve: [],
            participations: [],
            stages: [],
        }),
        computed: {
            groupedReserve(){
                return _.mapValues(_.groupBy(this.reserve, 'status'),
                    status_group => _.groupBy(status_group, 'category')
                );
            },
        },
        mounted: function () {
            this.$http.get(process.env.APP_URL + 'api/participation').then(function (resp) {
                    _.assign(this, resp.data);
                },
                function (resp) {
                    console.log(resp);
                });
        },
        methods: {
            filterParticipations(r) {
                return _.mapValues(_.filter(this.participations, ['reservist', r.id]),
                    participation => ({
                        id: participation.id,
                        stage: _.find(this.stages, ['id', participation.stage]),
                        step_selected: participation.step,
                    })
                );
            }
        },

        components: {
            'reservist-row': ReservistRow
        }
    }
</script>

<style>
    td.callout
    {
        border: 0px;
    }
</style>