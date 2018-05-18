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
                    n=> {F.refresh_auth(n)} ,
                    n=>console.log(n)
                )
        },
        logout : ()=>{
            $http.post('/api/v1.4/logout/')
                .then(
                    n=>F.refresh_auth(n),
                    n=>console.log(n)
                )
        },
        refresh_auth : async(res)=> {
            res = res || await $http.get('/api/v1.4/authorization/')
            $rootScope.authorization = res.data.authorization;
            $rootScope.user = res.data.user || {};
        }
    }
    
    $rootScope.$on('authorization.refresh', ()=>F.refresh_auth())
    return F
    
}]