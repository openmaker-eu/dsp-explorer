import * as _ from 'lodash'
import * as d3 from 'd3';


let template = `
    <div class="col-md-12">
        <h1>
            {$ project.name $}
            <a href="{$ '/profile/project/'+project.id $}" class="btn custom-button pull-right">Edit</a>

        </h1>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: { projectid : '=', profileid : '=' },
        controller : ['$scope', '$http', function($scope, $http ) {

            let url = '/api/v1.3/project/' + $scope.projectid
            $scope.projects = []
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.project = res.data.result[0] || ''
                    console.log($scope.project)
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            $scope.get_data(url)
        }]
    }
}]



