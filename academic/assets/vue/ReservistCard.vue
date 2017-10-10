<template>
  <div class="reservist-row">
    <div class="reservist-card">
      <div class="name">{{ reservist.name }}</div>
      <div class="info">
        <div class="position">{{ reservist.position }}</div>
        <div>{{ reservist.department.short_name || reservist.department.name }}</div>
      </div>

    <div class="links">
      <a :href="reservist.admin_url"><i class="fi-pencil"></i></a>
      <a :href="reservist.personal_page"><i class="fi-web"></i> </a>
      <a :href="mailto"><i class="fi-at-sign"></i></a>
    </div>

    <div class="quota" :class="{'callout alert': warnings.department}">
        {{ warnings.department ? 'Превышение квоты' : 'Квота соблюдена' }} <i class="fi-torsos-all"></i> 
    </div>
    <div class="age" :class="{'callout alert': warnings.age}"> 
      {{ ageFormat }} <i class="fi-results-demographics"></i>
    </div>
    <div class="experience" :class="{'callout alert': warnings.hse}">
      Стаж {{ reservist.experience }} <i class="fi-home"></i>
    </div>
    <div class="phd" title="Учёная степень" :class="{'callout alert': warnings.phd}">
      {{ reservist.phd }} <i class="fi-book-bookmark"></i>
    </div>
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