import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div map-lazy-load="https://maps.google.com/maps/api/js"
         style="position:relative;
         padding-bottom:50%;">
        <ng-map style="position:absolute; top:0; left:0; bottom:0; right:0; width:100%; height: 100%;"
                center="46.8815115,9.1133242"
                zoom="5"
        >
            <marker position="{$ place.lat $},{$ place.long $}" ng-repeat="place in places"></marker>
        </ng-map>

    </div>

`

export default [function(){
    
    return {
        template:template,
        controller : ['$scope','$http', function($scope, $http){
            $scope.places=[]
            
            $http.get('/api/v1.1/get_places').then( (results)=>{
                $scope.places = _.map( results.data.places, e => JSON.parse(e) )
                console.log('Results :', $scope.places)
            })
        }]
    }
    
}]