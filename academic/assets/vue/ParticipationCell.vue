<template>
  <div class="reserve-cell callout" :class="{warning: deadlineWarning}">
      <a :href="stage.admin_url">{{ stage.name }}</a>
      <select v-model="step_id" >
        <option v-for="step in stage.steps" :value="step.id">{{ step.name }}</option>
      </select>
    <span class="fi-calendar float-right"> {{ stage.deadline }}
      <a @click="reminder()" v-if="deadlineWarning" class="fi-mail"></a>
    </span>
  </div>
</template>

<script>
  import _ from 'lodash'
  export default
  {
    name: 'participation-cell',
    props: ['participation'],
    data() {
      return {
        step_id: this.participation.step_selected,
        stage: this.participation.stage
      }
    },
    computed: {
      step() {
        return _.find(this.stage.steps, ['id', this.step_id]);
      },
      deadlineWarning() {
        return this.stage.warning && !this.step.is_final;
      },
    },
    methods: {
      reminder() {
        this.$modal.show('mailer', {participation: this.participation});
      },
    },
    watch: {
        step: function (step) {
           this.$http.patch(process.env.APP_URL + `api/participation/${this.participation.id}/`, {step: step.id});
        }
      }
  }
</script>

