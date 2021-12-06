new Vue({
  el: "#app",
  delimiters: ["${", "}"],
  data: {
    dropFiles: null,
  },
  methods: {
    deleteDropFile() {
      this.dropFiles = null;
    },
    uploadFile() { 
      console.log(this.dropFiles);
      var xhr=new XMLHttpRequest();
      xhr.open('post','/upload_song',true);
      const form = new FormData();
      form.append('file',this.dropFiles);
      xhr.send(form);
    },
  },
});
