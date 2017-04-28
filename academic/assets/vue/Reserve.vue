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
                    <th v-for="pstage in table.participations"></th>
                    </thead>
                    <tr is="reservist-row" v-for="r in table.reservists" :res="r" :key="r.url"></tr>
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
            reserve: []
        }),
        computed: {
            groupedReserve(){
                return _.mapValues(_.groupBy(this.reserve, 'status'),
                    status_group =>
                        _.mapValues(_.groupBy(status_group, 'category'),
                            c_group => ({
                                participations: c_group[0].participations,
                                reservists: c_group
                            })
                        ));
            },
        },
        mounted: function () {
            this.$http.get(process.env.APP_URL + 'api/reserve/').then(function (resp) {
                    this.reserve = resp.data;
                },
                function (resp) {
                    console.log(resp);
                });
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