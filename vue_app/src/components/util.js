
import { useRouter } from 'vue-router'
const router = useRouter()

export function userValidation(){
    const token = localStorage.getItem('token');
    console.log(token)
    if(token == null){
        router.push({ path: "/login" });
    }else{
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    return token
}