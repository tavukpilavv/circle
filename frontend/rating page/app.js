
const App = {
  
  data() {
    return {
      // Event tamamlandı mı kontrolü (şimdilik true)
      eventCompleted: true,
      // Dialog görünürlüğü
      dialogVisible: false, 
      rating: 0,
      textarea: ""
    }
  },
  
  mounted() {
    // Body'yi göster (Vue yüklendi)
    if (document.body) {
      document.body.style.opacity = '1';
    }
    
    // Event tamamlandıysa pop-up'ı göster
    if (this.eventCompleted) {
      this.showFeedbackDialog();
    }
  },
  
  watch: {
    dialogVisible(newVal) {
      if (newVal) {
        // Dialog açıldığında style'ları düzelt
        this.$nextTick(() => {
          this.fixDialogStyles();
        });
      }
    }
  },
  
  methods: {
    
    // Feedback dialog'unu göster
    showFeedbackDialog() {
      // Dialog'u göster (nextTick ile Vue render'ını bekliyoruz)
      this.$nextTick(() => {
        setTimeout(() => {
          this.dialogVisible = true;
          // Dialog açıldıktan sonra body style'larını düzelt
          this.$nextTick(() => {
            this.fixDialogStyles();
          });
        }, 300);
      });
    },
    
    // Dialog style'larını düzelt
    fixDialogStyles() {
      setTimeout(() => {
        // Dialog body'yi bul ve style'larını düzelt
        const dialogBody = document.querySelector('.el-dialog__body');
        if (dialogBody) {
          dialogBody.style.maxHeight = 'none';
          dialogBody.style.height = 'auto';
          dialogBody.style.overflow = 'visible';
          dialogBody.style.overflowY = 'visible';
          dialogBody.style.overflowX = 'visible';
        }
        
        // Tüm içeriği görünür yap
        const feedbackContent = document.querySelector('.feedback-content');
        if (feedbackContent) {
          feedbackContent.style.display = 'block';
          feedbackContent.style.visibility = 'visible';
          feedbackContent.style.opacity = '1';
        }
        
        // Textarea'yı görünür yap
        const textarea = document.querySelector('.feedback-textarea');
        if (textarea) {
          textarea.style.display = 'block';
          textarea.style.visibility = 'visible';
          textarea.style.opacity = '1';
        }
      }, 100);
    },
    
    // Cancel butonuna tıklandığında
    cancelFeedback() {
      // Diyaloğu kapat ve verileri sıfırla
      this.dialogVisible = false;
      this.rating = 0;
      this.textarea = "";
    },

    // Submit butonuna tıklandığında
    submitFeedback() {
      // Verileri konsola yazdır
      console.log('User Rating:', this.rating);
      console.log('User Feedback:', this.textarea);

      // Başarı mesajı göster
      ElMessage.success('Feedback submitted successfully!');

      // Data'yı sıfırla ve diyaloğu kapat
      this.dialogVisible = false;
      this.rating = 0;
      this.textarea = "";
    }
  }
};

// Vue motorunu çalıştır
const app = Vue.createApp(App);
app.use(ElementPlus);
app.mount('#app');