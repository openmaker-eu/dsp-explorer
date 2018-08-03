import * as _ from 'lodash'

export default ['$http', '$rootScope', '$cookies', function($http, $rootScope, $cookies){
    
    let F = {
        login : (username, password)=>{
            $http({
                    method: 'POST',
                    url: '/api/v1.4/login/',
                    data: { username: username, password: password },
                })
                .then(
                    n=>{
                        $rootScope.$emit('authorization.refresh')
                        $rootScope.message = { text:'You have successfully login', type:'success'}
                        $cookies.remove('chatbot_last_open_date');
                    },
                    n=>{ console.log(n); $rootScope.message = { text:'Some problem occour during login please try again', type:'danger'}}
                )
        },
        logout : ()=>{
            $http.post('/api/v1.4/logout/')
                .then(
                    n=>{
                        $rootScope.$emit('authorization.refresh')
                        $rootScope.message = { text:'You have successfully logged out', type:'success'}
                        $cookies.remove('chatbot_last_open_date');
                    },
                    n=>{ console.log(n); $rootScope.message = { text:'Some problem occour during logout please try again', type:'danger'}}
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