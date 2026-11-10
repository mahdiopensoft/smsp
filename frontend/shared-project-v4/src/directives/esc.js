export default {
    mounted(el,binding) {
        el.__escHandler__ = (e) =>{
            if(e.key === "Escape"){
                if(typeof binding.value === "function"){
                    binding.value()
                }else if(binding.value && binding.value.active && typeof binding.value.handler === "function"){
                    if(binding.value.active){
                         binding.value.handler()
                    }
                }
            }
        };
        window.addEventListener("keydown",el.__escHandler__);        
        
    },
    unmounted(el){
        window.removeEventListener("keydown",el.__escHandler__)
    }
}