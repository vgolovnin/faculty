<template>
  <modal name="mailer" classes="modal-mailer" :width="width" :height="height" @before-open="beforeOpen">
    <p class="status">{{ status }}</p>
    <form @submit.prevent="sendMail">
      <div class="row">
        <div class="medium-6 columns">
          <label>Кому
            <input type="email" v-model="mail.to"/>
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
            <input type="text" v-model="mail.subject"/>
          </label>
        </div>
      </div>

      <div class="foot row">
        <label>Текст письма
          <textarea v-model="mail.text"></textarea>
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
    props: {
      width: {
        type: Number,
        default: 450
      },
      height: {
        type: Number,
        default: 700
      }
    },
    data: () => ({
      participationId: 0,
      mail: {from: "", to: "", subject: "", text: ""},
      status: ''
    }),
    methods: {
      async beforeOpen(event) {
        this.participationId = event.params.participation.id
        this.status = ''
        let resp = await this.$http.get(process.env.APP_URL + `mailers/participation/${this.participationId}`)
        _.assign(this.mail, resp.data);
      },
      async sendMail() {
        console.log('gonna send', this.mail);
        let resp = await this.$http.post(process.env.APP_URL + 'mailers/send_reminder', _.pick(this.mail, ['to', 'subject', 'text']))
        console.log(resp)
        this.status = resp.body.error ? resp.body.error : 'Письмо отправлено!'
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

    .status {
      height: 3em;
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