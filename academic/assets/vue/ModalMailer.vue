<template>
    <modal name="mailer" classes="modal-mailer" :width="width" :height="height" @before-open="beforeOpen">
        <form>
            <div class="row">
                <div class="medium-6 columns">
                    <label>Кому
                        <input type="email" :value="mail.to"/>
                    </label>
                </div>
                <div class="medium-6 columns">
                    <label>От кого
                        <input type="email" disabled :value="mail.from"/>
                    </label>
                </div>
            </div>
            <div class="row">
                <div class="small-12 columns">
                    <label>Тема
                        <input type="text" :value="mail.subject"/>
                    </label>
                </div>
            </div>

            <div class="foot row">
                <label>Текст письма
                    <textarea>{{ mail.text }}</textarea>
                </label>
                   <div class="float-right"><input type="submit" class="button"/></div>
            </div>
        </form>
    </modal>
</template>

<script>
    export default
    {
        name: 'modal-mailer',
        data: () => ({
          mail: {to: "", subject:"", text:""},
          width: 450,
          height: 650
        }),
        methods:{
            beforeOpen(event)
            {
                this.$http.get(process.env.APP_URL + 'mailers/participation/' + event.params.participation.id).
                then(function (resp) {
                    _.assign(this.mail, resp.data);
                },
                function (resp) {
                    console.log(resp);
                });
            }
        }
    }
</script>

<style lang="scss">
    .modal-mailer{
        padding: 10px;
        background-color: white;
        .foot.row {
            margin: 10px;
        }

        form {
            label {
                text-align: left;
            }
            textarea {
                width: 420px;
                height: 300px;
            }
        }
    }
</style>