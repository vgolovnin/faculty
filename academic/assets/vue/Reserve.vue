<template>
  <div class="reserve-table">
    <div v-for="(categories,status) in groupedReserve">
      <h4 class="status-header">Статус участия: {{ status }}</h4>
      <div v-for="(table, category) in categories" class="clearfix">
        <h5>{{ category }}</h5>
        <reservist-card v-for="reservist in table"
          :key="reservist.id" :reservist="reservist"
          :participations="filterParticipations(reservist)"
          :warnings="reservist.warnings">
          </reservist-card>
      </div>
    </div>
  </div>
</template>

<script>
  import _ from 'lodash'
  import ReservistCard from './ReservistCard.vue'
  export default
  {
    name: "ReserveTable",
    data: () => ({
      academic : {
        reserve: [],
        participations: [],
        stages: []
      }
    }),
    computed: {
      groupedReserve(){
        return _.mapValues(_.groupBy(this.academic.reserve, 'status'),
          status_group => _.groupBy(status_group, 'category')
        );
      },
    },
    mounted() {
      this.$http.get(process.env.APP_URL + 'api/participation').then(function (resp) {
          _.assign(this.academic, resp.data);
        },
        function (resp) {
          if (resp.status === 403) {
            document.location.replace('/admin/login')
          } 
        });
    },
    methods: {
      filterParticipations(r) {
        return _.mapValues(_.filter(this.academic.participations, ['reservist', r.id]),
          participation => ({
            id: participation.id,
            stage: _.find(this.academic.stages, ['id', participation.stage]),
            step_selected: participation.step,
          })
        );
      }
    },

    components: {
      'reservist-card': ReservistCard
    }
  }
</script>
