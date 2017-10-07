<template>
  <div class="reservist-row">
    <div class="reservist-card callout reserve-cell" @click="expanded = !expanded">
      <div class="name">{{ reservist.name }}</div>
      <span class="links">
        <a :href="reservist.admin_url"><i class="fi-pencil"></i></a>
        <a :href="reservist.personal_page"><i class="fi-web"></i> </a>
        <a :href="mailto"><i class="fi-at-sign"></i></a>
      </span>
      <em>{{ reservist.position }}</em>

      <transition name="slide-fade">
        <div v-if="expanded">
          <div class="callout float-right" :class="{warning:warnings.department}">
            <i class="fi-alert" title="Квота" v-if="warnings.department"></i>
            {{ reservist.department }}
          </div>
          <div class="float-left">
            <div class="callout age" title="Возраст" :class="{alert: warnings.age}">
              <i class="fi-results-demographics"></i>
              {{ ageFormat }}
            </div>
            <div class="callout experience" title="Стаж работы" :class="{alert: warnings.hse}">
              <i class="fi-home"></i>
              {{ reservist.experience }}
            </div>
            <div class="callout phd" title="Учёная степень" :class="{alert: warnings.phd}">
              <i class="fi-book-bookmark"></i>
              {{ reservist.phd }}
            </div>
          </div>
        </div>
      </transition>
    </div>
    <participation-cell v-for="participation in sortedParticipations"
      :key="participation.id"
      :participation="participation"
      :readonly="false">
    </participation-cell>
  </div>
</template>

<script>
  export default
  {
    name: "ReservistCard",
    props: ['reservist', 'warnings', 'participations'],
    data() {
      return {
        expanded: _.find(_.values(this.warnings, true)) === true
      }
    },
    computed: {
      sortedParticipations() {
        return _.sortBy(this.participations, "stage.deadline");
      },
      mailto() {
        return 'mailto:' + this.reservist.email;
      },
      ageFormat() {
        const mod = this.reservist.age % 10;
        return this.reservist.age + ' ' + (!mod || mod >= 5 ? "лет" : (mod == 1 ? "год" : "года"));
      }
    },
    components: {
      'participation-cell': require('./ParticipationCell.vue'),
    }
  }
</script>

<style lang="scss">
  .reservist-row
  {
    white-space: nowrap;
    clear: both;
    font-size: 0;

    .reserve-cell {
      white-space: normal;
      display: inline-block;
      vertical-align: top;
      font-size: 0.8rem;
      padding: 4px 12px;
      margin-bottom: 0.2rem;
      margin-left: 0.2rem;
      width: 150px;
      min-height: 8rem;
      max-height: 230px;
      /*height: 230px;*/
      border: 1px solid rgba(10, 10, 10, 0.25);
      select, label {
        font-size: 0.8rem;
      }

      &.reservist-card {
        width: 350px;
        height: auto;

        .callout {
          padding: 4px;
          margin: 0.25rem 0;
          width: 160px;
        }
        
        .links{
          position: absolute;
          font-size: 1.25rem;
          top: 0px;
          right: 10px;
        }
        .name {
          font-size: 1.2rem;
          width: 220px;
          float: left;
        }
      }

      em {
        text-align: right;
        position: absolute;
        top: 1.5rem;
        right: 10px;
        width: 7rem;
      }

      &.callout {
        label {
          height: 6rem;
          a {
            display: block;
            height: 3rem;
          }
        }
      }
    }
  }
</style>