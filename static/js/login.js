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
    validateLogin() {
      let username = document.forms[formType.toLowerCase()]["username"].value;
      let password = document.forms[formType.toLowerCase()]["password"].value;
      if ((username === "") | (password === "")) {
        alert("Please enter a username and password.");
        return false;
      }
      return true;
    },
  },
});
