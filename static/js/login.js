new Vue({
  el: "#app",
  delimiters: ["${", "}"],
  data: {
    formType: "Login",
  },
  methods: {
    updateFormType() {
      document.getElementById(this.formType).style.display = "none";
      this.formType = this.formType === "Login" ? "Register" : "Login";
      document.getElementById(this.formType).style.display = "block";
    },
  },
});
