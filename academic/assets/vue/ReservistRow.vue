<template>
    <tr class="reservist-row">
        <td><a :href="res.admin_url">{{ res.name }}</a>
            <a :href="res.personal_page" class="fi-web"></a>
            <a :href="mailto(res.email)" class="fi-at-sign"></a>
            <div class="callout" v-bind:class="{alert: res.warnings.age}">Возраст: {{ res.age }}</div>
            <div class="callout" v-bind:class="{alert: res.warnings.hse}">Стаж: {{ res.experience }}</div>
            <div class="callout" v-bind:class="{alert: res.warnings.phd}">Уч. степень: {{ res.phd }}</div>
        </td>
        <td class="callout" v-bind:class="{warning: res.warnings.department}">
            <span style="font-style:italic;">{{ res.position }}</span><br/>
            {{ res.department }}
        </td>
        <td style="width:200px;" class="callout" v-bind:class="{warning: stagewarning(pstage)}"
            v-for="pstage in datesort(res.participations)">
            <a :href="pstage.stage.admin_url">{{ pstage.stage.name }}</a>
            <div class="fi-calendar"> {{ pstage.stage.deadline }}
                <a :href="reminder(res, pstage.stage)" v-if="!pstage.disabled" class="fi-mail"
                   onclick="return confirm('Send mail')"></a>
            </div>
            <select v-model="pstage.step_selected" :disabled="pstage.disabled">
                <option v-for="step in pstage.stage.steps" :value="step.id">{{ step.name }}</option>
            </select>
        </td>
    </tr>
</template>

<script>
    export default
    {
        name: "ReservistRow",
        props: ['res'],
        methods: {
            mailto(email){
                return 'mailto:' + email;
            },
            datesort(part){
                return _.sortBy(part, "stage.deadline");
            },
            stagewarning(pstage)
            {
                return pstage.stage.warning && (pstage.step_selected == _.first(pstage.stage.steps).id);
            },
            reminder(res, stage)
            {
                return "reminders/reservist/" + res.id + "/stage/" + stage.id;
            }
        },
        watch: {
            'res.participations': {
                handler: function () {
                    this.$http.patch(this.res.url, {
                        'participations': this.res.participations
                    })
                },
                deep: true
            },
        }
    }
</script>

<style>

    .reservist-row td > .callout
    {
        padding: 4px 16px;
        margin-bottom: 4px;
    }
</style>