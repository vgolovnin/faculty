<template>
    <div class="reserve-cell callout" v-bind:class="{warning: stagewarning}">

        <label v-if="!readonly" >
            <a :href="stage.admin_url">{{ stage.name }}</a>
            <select v-model="step_id" >
                <option v-for="step in stage.steps" :value="step.id">{{ step.name }}</option>
            </select>
        </label>
        <div v-else>{{ stage.name }}
            <h5 class="text-center">{{ step.name }}</h5></div>
            <span class="fi-calendar float-right"> {{ stage.deadline }}
                <a @click="reminder()" v-if="stagewarning" class="fi-mail"></a>
            </span>
    </div>
</template>

<script>
    import _ from 'lodash'
    export default
    {
        name: 'participation-cell',
        props: ['participation', 'readonly'],
        data(){
            return {
                step_id: this.participation.step_selected,
                stage: this.participation.stage
            }
        },
        computed: {
            step(){
                return _.find(this.stage.steps, ['id', this.step_id]);
            },
            stagewarning()
            {
                return this.stage.warning && !this.step.is_final;
            },
        },
        methods: {
            reminder()
            {
                this.$modal.show('mailer', {participation: this.participation});
            },
        },
        watch:
            {
                step: function (step) {
                     this.$http.patch(process.env.APP_URL + `api/participation/${this.participation.id}/`, {step: step.id});
                }
            }
    }
</script>

