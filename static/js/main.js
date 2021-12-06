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
      xhr.onreadystatechange = function()
      {
          if (xhr.readyState == 4 && xhr.status == 200)
          {
              console.log("Redirecting.")
              window.location.href = xhr.responseURL;
          }
      };
      console.log(xhr);
    },
  },
});
