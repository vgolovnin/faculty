<template>
    <div class="reservist-row">
        <reservist-card :res="res" :warnings="this.warnings"></reservist-card>
        <participation-cell v-for="p in participations" :key="p.id"
                            :participation="p"  :readonly="false">
        </participation-cell>
    </div>
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
        },
        components: {
            'reservist-card': require('./ReservistCard.vue'),
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