<template>
    <tr class="reservist-row">
        <td><a :href="res.admin_url">{{ res.name }}</a>
            <a :href="res.personal_page" class="fi-web"></a>
            <a :href="mailto" class="fi-at-sign"></a>
            <div class="callout fi-results-demographics" title="Возраст" v-bind:class="{alert: warnings.age}"> {{ res.age }}</div>
            <div class="callout fi-home" title="Стаж работы" v-bind:class="{alert: warnings.hse}"> {{ res.experience }}</div>
            <div class="callout fi-pencil" title="Учёная степень" v-bind:class="{alert: warnings.phd}"> {{ res.phd }}</div>
        </td>
        <td class="callout">
            <span style="font-style:italic;">{{ res.position }}</span><br/>
            {{ res.department }}
            <div class="callout warning fi-alert" v-if="warnings.department"> Квота</div>
        </td>
        <td is="participation-cell" v-for="p in participations" :stage="p.stage" :step_default="p.step_selected" :id="p.id">
        </td>
    </tr>
</template>

<script>
    export default
    {
        name: "ReservistRow",
        props: ['res', 'warnings', 'part'],
        computed: {
            participations() {
                return _.sortBy(this.part, "stage.deadline");
            },
            mailto(){
                return 'mailto:' + this.res.email;
            },
        },
        components: {
            'participation-cell': require('./ParticipationCell.vue'),
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