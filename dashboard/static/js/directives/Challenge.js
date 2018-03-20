import * as _ from 'lodash'
import * as d3 from 'd3';

let template = require('../../templates/challenge_details.html');

export default [function(){
    return {
        template:template,
        scope: { id : '=' },
        controller : ['$scope', '$http', '$sce', function($scope, $http, $sce){
            $scope.get_data = ()=> Promise
                    .all([
                        $http.get('/api/v1.3/challenge/'+$scope.id+'/'),
                        $http.get('/api/v1.3/interest_ids/')
                    ])
                    .then(
                        res=>{
                            res[0].data.details = res[0].data.details && $sce.trustAsHtml(res[0].data.details)
                            $scope.challenge = res[0].data || {}
                            $scope.interested_ids = res[1].data || []
                            $scope.$apply(()=>$(window).trigger('resize'))
                        },
                        err=>console.log('Error: ', err)
                    )
    
            $scope.get_data()
            
            $scope.click_interest = (challenge) =>
                ($scope.is_interested(challenge) ?
                    $http.delete('/api/v1.3/interest/challenge/'+challenge.id+'/') :
                    $http.post('/api/v1.3/interest/challenge/'+challenge.id+'/')
                )
                .then(res=>$scope.get_data(),err=>console.log(err))
            
            $scope.is_interested = (challenge)=>$scope.interested_ids && $scope.interested_ids.indexOf(challenge.id) > -1
 
        }]
    }
}]



