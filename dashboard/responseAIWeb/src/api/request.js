//二次封装axios
import axios from "axios";


//也可以不创建实例  直接使用axios   最后要导出axios而不是reques
// axios.defaults.baseURL=''
// axios.interceptors.request

//创建实例并配置
const request = axios.create({
    //配置对象

    //基础路径
   // baseURL:'https://wdm.orangelabschina.cn:8057',
    baseURL:'http://'+window.location.hostname+':8011',
    // baseURL:'/api',
    //超时时间
    timeout:7000
});
//请求拦截器
request.interceptors.request.use((config)=>{
    return config;
})
//响应拦截器
request.interceptors.response.use((res)=>{
    //成功的回调函数：服务器响应数据回来以后，响应拦截器可以检测到，可以做一些事
    //进度条结束
    return res.data
},(error)=>{
    //响应失败的回调函数
    console.log(error);
    return Promise.reject(new Error('fail'))
})

//对外暴露
export default request;
