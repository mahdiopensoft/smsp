//عرض علامة العين واخفاء الارقام في حقول كلمة المرور
export default{
data()
{
  return{
    _passwordStates:{}
  };
},
methods: {
  togglePassword(filedName='default'){
    this._passwordStates[filedName] = !this._passwordStates[filedName];
  },
  getPasswordType(filedName='default'){
     return this._passwordStates[filedName] ? 'text' : 'password';
  },
  getPasswordIcon(filedName='default'){
    return this._passwordStates[filedName] ? 'mdi-eye' : 'mdi-eye-off';
 },
},
};
