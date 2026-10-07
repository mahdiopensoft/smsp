import axios from "axios"



 
export  async function getCurrentYear(){
    return await axios('academic-affairs/academic-year/get-current-year/').then(response=>{        
        return response.data
    })
}
