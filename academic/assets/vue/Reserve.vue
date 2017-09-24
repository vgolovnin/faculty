<template>
    <div class="reserve-table">
        <div v-for="(categories,status) in groupedReserve">
            <h4 class="status-header">Статус участия: {{ status }}</h4>
            <div v-for="(table, category) in categories" class="clearfix">
                <h5>{{ category }}</h5>
                <reservist-row v-for="r in table" :key="r.id" :res="r" :part="filterParticipations(r)" :warnings="r.warnings"></reservist-row>
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
                    if (resp.status === 403) {
                        document.location.replace('/admin/login')
                    } 
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
    .reserve-table{ margin: 2% 0 0 5%;}
    .status-header {margin-left: -3%;}
</style>
