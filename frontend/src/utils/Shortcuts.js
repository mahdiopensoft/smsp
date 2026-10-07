import { reactive } from "vue";
const Key_MAP={
  'alt+s':'saveData',
  'alt+r':'getData',
  'alt+n':'create',
  'alt+c':'handleSubmit',
  'escape':'handleCancel',
  'f2':'handleTypePrint',
  'f4':'ExportExcel',
};
const eventBus = reactive({
  listeners:{}
});
export default {
  install(app){
    window.addEventListener('keydown',(event)=>{
      let key = event.key?.toLowerCase();
      if(event.code?.startsWith('key')){
        key = event.code.slice(3).toLowerCase();
      }
      const keys=[];
      if(event.altKey) keys.push('alt');
      if(event.ctrlKey) keys.push('ctrl');
      if(key !== 'alt' && key !== 'ctrl') keys.push(key);
      const combo = keys.join('+');
      if(Key_MAP[combo]){
        const methodName = Key_MAP[combo];
        const activeTag = document.activeElement.tagName;
        if(['INPUT','TEXTAREA'].includes(activeTag)&& !event.altKey && !event.ctrlKey && key !== 'escape'){
          return;
        }
        if(eventBus.listeners[methodName] && eventBus.listeners[methodName].length >0){
          event.preventDefault();
          const lastListeners = eventBus.listeners[methodName][eventBus.listeners[methodName].length-1];
          lastListeners();
        }
      }
    });
    app.mixin({
      mounted() {
        const methodNames = Object.values(Key_MAP);
        methodNames.forEach(name=>{
          if(typeof this[name] === 'function'){
            if(!eventBus.listeners[name]){
              eventBus.listeners[name]=[];
            }
            eventBus.listeners[name].push(this[name]);
          }
        });
      },
      unmounted() {
        const methodNames = Object.values(Key_MAP);
        methodNames.forEach(name=>{
          if(typeof this[name] === 'function' && eventBus.listeners[name]){
            const index = eventBus.listeners[name].indexOf(this[name]);
            if(index > -1){
             eventBus.listeners[name].splice(index,1);
            }

          }
        });
      },

    })
    app.config.globalProperties.$onKey = function (name,callback){
    if(!eventBus.listeners[name]){
      eventBus.listeners[name] = [];
    }
    eventBus.listeners[name].push(callback);
    }
  }
}
