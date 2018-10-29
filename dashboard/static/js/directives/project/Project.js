let _ = require('lodash')

let template = require('./templates/Project.html')


export default [function(){
    return {
        template:template,
        scope: { projectid : '=', tags: '=' },
        controller : ['$scope', '$rootScope', '$http', '$sce', '$window', 'toastr', function($scope, $rootScope, $http, $sce, $window, toastr){

        // form data
        $scope.data = {}
        
        
        $scope.create_or_update_project = () => {
            let form =  document.getElementById('project_form')
            
            $scope.project_form.$valid && $http({
                method: 'POST',
                url: $scope.url,
                data: new FormData(form),
                headers: {'Content-Type': undefined },
                transformRequest: angular.identity
            })
            .then(r=>
                $window.location.href = '/profile'
            )
            .catch(
                r=>{
                    console.log('Error', r);
                    console.log('Error', r.data.message);
                    $rootScope.alert_message ('danger', _.get(r, 'data.message'))
                }
            )
            
        }

        $scope.get_data = (url) => {
            $http.get(url).then(res => {
                $scope.data = res.data.result[0] || {}
                $scope.data.start_date = new Date(res.data.result[0].start_date)
                if ($scope.data.end_date == '' || $scope.data.end_date == null) {
                    $scope.data.project_ongoing = true
                } else {
                    $scope.data.end_date = new Date(res.data.result[0].end_date)
                }
            })
        }

        // project image
        $scope.profileImageUpload = n=>$('#profile-image-input').trigger('click')

        // tags
        $scope.av_tags={ available:  $scope.tags  }

        // keep pushed
        $scope.push_bottom = () => { $scope.re_render }
    
    
        $scope.isFormValid = (form) => {
                if(!form || !form.hasOwnProperty('$$element')) return false
                // Display form errors
                form.$submitted = true;
                // Trigger validation
                _.each(form.$$controls, (field) => field.$validate())
                // Return validation status
                return _.get(form, '$valid')
        }

        // action based on create or update
        if ($scope.projectid) {
            $scope.url = '/api/v1.3/project/' + $scope.projectid + '/'
            // fill the template form with project information
            $scope.get_data($scope.url)
        } else {
            $scope.url = '/api/v1.3/project/'
        }

        }]
    }
}]



