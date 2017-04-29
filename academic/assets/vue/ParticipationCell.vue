<template>
    <td class="participation-cell callout" v-bind:class="{warning: stagewarning}">
    <a :href="stage.admin_url">{{ stage.name }}</a>
            <div class="fi-calendar"> {{ stage.deadline }}
                <!--<a :href="reminder(res, participation.stage)" v-if="!participation.disabled" class="fi-mail"-->
                   <!--onclick="return confirm('Send mail')"></a>-->
            </div>
            <select v-model="step_selected" :disabled="disabled">
                <option v-for="step in stage.steps" :value="step.id">{{ step.name }}</option>
            </select>
    </td>
</template>

<script>
    export default
    {
        name: 'participation-cell',
        props: ['id', 'stage', 'step_default'],
        data(){
            return {
                disabled: false,
                step_selected: this.step_default
            }
        },
        computed: {
            stagewarning()
            {
                return this.stage.warning &&
                    !_.find(this.stage.steps, ['id', this.step_selected]).is_final
            },
//            reminder(res, stage)
//            {
//                return "reminders/reservist/" + res.id + "/stage/" + stage.id;
//            },
        },
        watch:
            {
                step_selected: function (step) {
                     this.$http.patch(process.env.APP_URL + `api/participation/${this.id}/`, {step: step});
                }
            }
    }
</script>

<style>
    .participation-cell {
        width:200px;
    }
</style>