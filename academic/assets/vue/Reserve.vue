<template>
  <div class="reserve-table">
    <div v-for="(categories,status) in groupedReserve">
      <h4 class="status-header">Статус участия: {{ status }}</h4>
      <div v-for="(table, category) in categories">
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

<style lang="scss">
  .reserve-table {
    width: 1450px;
    margin: 12px 0 0 16px;
    .reservist-row {
        display: flex;
        flex-flow: row;
      .reservist-card {
          width: 20rem;
          height: 10rem;
          display: flex;
          flex-flow: column wrap;
          justify-content: space-evenly;

          .name {
            order:1;
            max-width: 9rem;
            line-height: 1.2rem;
            flex-basis: 4rem;
            font-size: 1.15rem;
          }

          .info {
            order: 2;
            max-width: 9rem;
            flex-basis: 4rem;

          .position {
            font-style: italic;
            }
          }
          .links{
            order: 3;
            font-size: 1.15rem;
          }
          .age {
            order: 5;
          }
          .experience {
            order: 6;
          }
          .phd {
            order: 7;
          }
          .quota {
            order: 8;
          }
          .age, .experience, .phd, .quota, .links {
            max-width: 9.5rem; 
            flex-basis: 1.5rem;
            text-align: right;
          }
          .callout {
            padding: 0.1rem;
            margin: 0.1rem 0;
          }
        }

      .reserve-cell {
        width: 10rem;
        height: 10rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        a {
          height: 2rem;
        }
      }

     .reservist-card, .reserve-cell {
        font-size: 0.75rem;
        border: 1px solid rgba(10, 10, 10, 0.25);
        margin: 0.1rem;
        padding: 0.5rem;
      }
    }
  }

</style>
