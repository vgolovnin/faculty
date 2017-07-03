<template>
    <div class="reservist-card callout reserve-cell" v-on:click="expanded = !expanded">
        <div class="name">{{ res.name }}</div>
        <span class="links">
            <a :href="res.admin_url"><i class="fi-pencil"></i></a>
            <a :href="res.personal_page"><i class="fi-web"></i> </a>
            <a :href="this.mailto"><i class="fi-at-sign"></i></a>
        </span>
        <em>{{ res.position }}</em>

        <transition name="slide-fade">
            <div v-if="expanded">
                <div class="callout float-right" :class="{warning:warnings.department}">
                    <i class="fi-alert" title="Квота" v-if="warnings.department"></i>
                    {{ res.department }}
                </div>
                <div class="float-left">
                    <div class="callout age" title="Возраст" v-bind:class="{alert: warnings.age}">
                        <i class="fi-results-demographics"></i>
                        {{ age_format }}
                    </div>
                    <div class="callout experience" title="Стаж работы" v-bind:class="{alert: warnings.hse}">
                        <i class="fi-home"></i>
                        {{ res.experience }}
                    </div>
                    <div class="callout phd" title="Учёная степень" v-bind:class="{alert: warnings.phd}">
                        <i class="fi-book-bookmark"></i>
                        {{ res.phd }}
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    export default
    {
        name: 'ReservistCard',
        props: ['res', 'warnings'],
        data: () => ({
            expanded: false
        }),
        computed: {
            mailto(){
                return 'mailto:' + this.res.email;
            },
            age_format()
            {
                const mod = this.res.age % 10;
                return this.res.age + ' ' + (!mod || mod >= 5 ? "лет" : (mod == 1 ? "год" : "года"));
            }
        }
    }
</script>

<style lang="scss">
    .reservist-row { 
        .reserve-cell {
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
        }
    }
</style>