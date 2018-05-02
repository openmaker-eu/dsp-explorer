import * as _ from 'lodash'

export default ['$http', '$rootScope',  function($http, $rootScope){
    
    let F = {
        login : (username, password)=>{
            
            $rootScope.$emit('authorization.reload')
            $rootScope.authorization = 1000;
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
            $rootScope.$emit('authorization.reload')
            $http.post('/api/v1.4/logout/')
                .then(
                    n=>F.refresh_page(n),
                    n=>console.log(n)
                )
        },
        refresh_page : (res)=> {
            $rootScope.authorization = res.data.authorization;
        }
    }
    return F
    
}]