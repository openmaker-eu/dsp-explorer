import * as _ from 'lodash'

export default ['$http', '$rootScope',  function($http, $rootScope){
    
    let F = {
        login : (username, password)=>{
            $http({
                    method: 'POST',
                    url: '/api/v1.4/login/',
                    data: { username: username, password: password },
                })
                .then(
                    n=>$rootScope.$emit('authorization.refresh'),
                    n=>console.log(n)
                )
        },
        logout : ()=>{
            $http.post('/api/v1.4/logout/')
                .then(
                    n=>$rootScope.$emit('authorization.refresh'),
                    n=>console.log(n)
                )
        },
        refresh_auth : async(res)=> {
            res = res || await $http.get('/api/v1.4/authorization/')
            $rootScope.authorization = res.data.authorization;
            $rootScope.twitter_auth = res.data.twitter_auth;
            $rootScope.user = res.data.user || {};
            $rootScope.bookmarks = _.get(res, 'bookmarks');
            $rootScope.twitter_name = _.get(res, 'twitter_screen_name');
        }
    }
    
    $rootScope.$on('authorization.refresh', ()=>F.refresh_auth())
    return F
    
}]