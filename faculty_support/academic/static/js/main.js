const Reserve = {
            name: 'Reserve_table',
            data: () => ({
              reserve: []
            }),
            computed:
                {
                      groupedReserve(){
                    return _.mapValues(_.groupBy(this.reserve, 'status'),
                        status_group =>
                            _.mapValues(_.groupBy(status_group, 'category'),
                                c_group => ({
                                    participations: c_group[0].participations,
                                    reservists: c_group
                                })
                            ));
                },
                },
                        mounted: function() {
                            this.$http.get('api/reserve/').then(function (resp) {
                                    this.reserve = resp.data;
                                },
                                function (resp) {
                                    console.log(resp);
                                });
                        },
            template: `<div>
                <div v-for="(categories,status) in groupedReserve">
        <h4 class="status-header">Статус участия: {{ status }}</h4>
        <div v-for="(table, category) in categories">
            <h5>{{ category }}</h5>
            <table>
                <thead>
                    <th style="width:300px;">Сотрудник</th>
                    <th style="width:200px;">Должность</th>
                    <th v-for="pstage in table.participations"></th>
                </thead>
                <tr is="reservist-row" v-for="r in table.reservists" :res="r" :key="r.url"></tr>
            </table>
        </div>
    </div>
    </div>
            `,
                        components:
                {
                    'reservist-row': {
                props: ['res'],
                template: `<tr class="reservist-row">
                       <td><a :href="res.admin_url">{{ res.name }}</a>
                        <a :href="res.personal_page" class="fi-web"></a>
                        <a :href="mailto(res.email)" class="fi-at-sign"></a>
                        <div class="callout" v-bind:class="{alert: res.warnings.age}">Возраст: {{ res.age }}</div>
                        <div class="callout" v-bind:class="{alert: res.warnings.hse}">Стаж: {{ res.experience }}</div>
                        <div class="callout" v-bind:class="{alert: res.warnings.phd}">Уч. степень: {{ res.phd }}</div>
                        </td>
                    <td class="callout" v-bind:class="{warning: res.warnings.department}">
                    <span style="font-style:italic;">{{ res.position }}</span><br/>
                    {{ res.department }}</td>
                    <td style="width:200px;" class="callout" v-bind:class="{warning: stagewarning(pstage)}" v-for="pstage in datesort(res.participations)">
                        <a :href="pstage.stage.admin_url">{{ pstage.stage.name }}</a>
                        <div class="fi-calendar"> {{ pstage.stage.deadline }}
                            <a :href="reminder(res, pstage.stage)" v-if="!pstage.disabled" class="fi-mail" onclick="return confirm('Send mail')"></a>
                        </div>
                        <select v-model="pstage.step_selected" :disabled="pstage.disabled">
                            <option v-for="step in pstage.stage.steps" :value="step.id">{{ step.name }}</option>
                        </select>
                    </td></tr>`,
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
                    'res.participations':{
                        handler: function () {
                            this.$http.patch(this.res.url, {
                                'participations': this.res.participations
                            })
                        },
                    deep: true
                    },
                }
            }
                }
        }

        const Reports = {
            name: 'Reports',
            data: () => ({
                report_stages: []
            }),
                        mounted: function() {

                this.$http.get('/api/reports/').then(function (resp) {
                    this.report_stages = resp.data;
                },
                    function(resp) {
                    console.log(resp);
                });

            },
            computed: {
                              reports(){
                    return _.mapValues(this.report_stages,
                        report_stage => (
                            _.mapValues(report_stage.templates,
                            template => ({
                                    name : template.name,
                                   stagename: report_stage.stagename,
                                   url: report_stage.url + "/template/" + template.id
                                }
                            ))
                        )
                    );
                }
            },
            template: `
                <div class="reports">
<h4 class="reports-header">Отчёты</h4>
    <ul v-for="report_stage in reports">
        <li v-for="report in report_stage">
             <a :href="report.url" class="fi-page-export-doc"> {{ report.stagename }} [{{ report.name }}]</a></a>
        </li>
    </ul>
</div>
            `
        }

        const routes =
            {
                '/' : Reserve,
                '/reports/': Reports,
            }

            var csrftoken = Cookies.get('csrftoken');
    Vue.http.headers.common['X-CSRFToken'] = csrftoken;

        var vm = new Vue({
            el: '#app',
            data: {
                currentRoute: window.location.pathname,
            },
            computed: {
                  ViewComponent () {
                     return routes[this.currentRoute] || NotFound
                    },
            },
            render (h) { return h(this.ViewComponent) },
        });

        window.addEventListener('popstate', () => {
  vm.currentRoute = window.location.pathname
});