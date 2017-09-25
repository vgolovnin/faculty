<template>
<nav>
    <div class="top-bar">
        <div class="top-bar-left">
            <ul class="dropdown menu" data-dropdown-menu>
                <li>
                    <router-link to="/">
                    <img :src="logo" alt="Академический кадровый резерв">
                    <span>Участники программы</span>
                    </router-link>
                </li>
                <li><span><a href="#" class="fi-plus" @click.prevent="al1()"> Добавить участника</a></span></li>
                <li><router-link to="/reports">Отчёты</router-link></li>
                <li><a href="/admin/">Администрирование</a></li>
            </ul>
        </div>
    </div>
    <modal name="ifr" :width=1000 :height=700>
    <iframe id="if0" src="/admin/academic/reservist/add?_popup=1" @load="al2()"
    width="1000" height="700" frameborder="0"></iframe>
    </modal>
</nav>
</template>

<script>
    import logo from '../logo.png'
    export default {
        name: 'navbar',
        data: () => ({
            logo: logo,
            frame: 0
        }),
        methods: {
            al1(){
                this.frame = 0;
                this.$modal.show('ifr');

            },
            al2(){
                if (!this.frame) this.frame++;
                else
                this.$modal.hide('ifr');
            },

        }
    }
</script>

<style lang="scss">
    .menu {
        li {
            margin: auto 0 auto 0;
        }
    }
</style>