<template>
        <nav>
        <div class="top-bar">
            <div class="top-bar-left">
                <ul class="dropdown menu" data-dropdown-menu>
                    <li class="menu-text">Академический <br/>кадровый резерв</li>
                    <li><span><router-link to="/">Участники программы</router-link>
                        <a href="#" class="fi-plus" @click.prevent="al1()"></a></span>
                    </li>
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
    export default {
        name: 'navbar',
        data: () => ({
           frame: 0,
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