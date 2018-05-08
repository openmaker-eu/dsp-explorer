import * as _ from 'lodash'

export default ['$http', '$rootScope',  function($http, $rootScope){
    
    let F = {
        login : (username, password)=>{
            $http({
                    method: 'POST',
                    url: '/api/v1.4/login/',
                    data: {
                        username: username,
                        password: password
                    },
                })
                .then(
                    n=> {F.refresh_page(n)} ,
                    n=>console.log(n)
                )
        },
        
        logout : ()=>{
            $http.post('/api/v1.4/logout/')
                .then(
                    n=>F.refresh_page(n),
                    n=>console.log(n)
                )
        },
        refresh_page : async(res)=> {
            res = res || await $http.get('/api/v1.4/authorization')
            console.log('Referesh:', res);
            $rootScope.authorization = res.data.authorization;
        }
    }
    
    $rootScope.$on('authorization.refresh', ()=>F.refresh_page())
    return F
    
}]