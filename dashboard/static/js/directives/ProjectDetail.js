import * as _ from 'lodash'
import * as d3 from 'd3';


let template = require('../../templates/project_details.html');

export default [function(){
    return {
        template:template,
        scope: { projectid : '=', profileid : '=' },
        controller : ['$scope', '$http', '$window', function($scope, $http, $window) {

            let model_object = 'project'
            $scope.url = '/api/v1.3/project/' + $scope.projectid
            $scope.projects = []
            $scope.show_form = false

            console.log('profileid: ' + $scope.profileid)

            $scope.open_close_form = (open_close) => {
                $scope.show_form = open_close
            }

            $scope.get_data = (url)=> Promise
                    .all([
                        $http.get(url),
                        $http.get('/api/v1.3/interest/ids/'+model_object)
                    ])
                    .then(
                        res=>{
                            console.log(res[0].data)
                            $scope.project = res[0].data.result[0] || []

                            $scope.interested_ids = res[1].data || []
                            console.log( $scope.interested_ids)
                            $scope.$apply(()=>$(window).trigger('resize'))
                        },
                        err=>console.log('Error: ', err)
                    )

            $scope.delete_project = (url) => {
                $http.delete(url).then(res => {
                    $window.location.href = '/profile';
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }

            $scope.get_data($scope.url)

            // set interest
            $scope.click_interest = (project) =>
                ($scope.is_interested(project) ?
                    $http.delete('/api/v1.3/interest/project/'+project.id+'/') :
                    $http.post('/api/v1.3/interest/project/'+project.id+'/')
                )
                .then(res=>$scope.get_data($scope.url),err=>console.log(err))


            // check if logged user is interested or not
            $scope.is_interested = (project) => {
                let result = $scope.interested_ids && $scope.interested_ids.indexOf(project.id) > -1
                console.log('result: ' + result)
                return result
            }


        }]
    }
}]



